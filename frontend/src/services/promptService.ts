import axios, { AxiosError } from 'axios';
import api from './api';

export interface Prompt {
    id: number;
    title: string;
    content: string;
}

export interface PromptPayload {
    title: string;
    content: string;
}

export interface ValidationError {
    [key: string]: string[];
}

export interface PromptServiceError {
    status?: number;
    message: string;
    validationErrors?: ValidationError;
}

const mapStatusMessage = (status: number): string => {
    switch (status) {
        case 400:
            return 'Error 400: Invalid request data.';
        case 401:
            return 'Error 401: Unauthorized.';
        case 403:
            return 'Error 403: Forbidden.';
        case 404:
            return 'Error 404: Endpoint not found.';
        case 500:
            return 'Error 500: Server-side failure.';
        default:
            return `HTTP error ${status}.`;
    }
};

const toServiceError = (error: unknown): PromptServiceError => {
    if (!axios.isAxiosError(error)) {
        return { message: 'Unexpected application error.' };
    }

    const axiosError = error as AxiosError<ValidationError>;

    if (axiosError.response) {
        return {
            status: axiosError.response.status,
            message: mapStatusMessage(axiosError.response.status),
            validationErrors:
                axiosError.response.status === 400
                    ? (axiosError.response.data as ValidationError)
                    : undefined,
        };
    }

    if (axiosError.request) {
        return { message: 'No response from backend. Check the connection.' };
    }

    return { message: 'Request configuration error.' };
};

export const getPrompts = async (): Promise<Prompt[]> => {
    try {
        const response = await api.get<Prompt[]>('/api/prompts/');
        return response.data;
    } catch (error) {
        throw toServiceError(error);
    }
};

export const createPrompt = async (payload: PromptPayload): Promise<Prompt> => {
    try {
        const response = await api.post<Prompt>('/api/prompts/', payload);
        return response.data;
    } catch (error) {
        throw toServiceError(error);
    }
};
