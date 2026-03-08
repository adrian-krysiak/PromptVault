import { useEffect, useState } from 'react';
import api from '../services/api';

interface Prompt {
    id: number;
    title: string;
    content: string;
}

const Dashboard = () => {
    const [items, setItems] = useState<Prompt[]>([]);
    const [error, setError] = useState('');

    useEffect(() => {
        api.get<Prompt[]>('/api/prompts/')
            .then((res) => setItems(res.data))
            .catch(() => setError('Frontend połączony, ale Backend jeszcze nie odpowiada – to normalne!'));
    }, []);

    return (
        <div style={{ padding: '20px', textAlign: 'center' }}>
            <h1>☁️ PromptVault Dashboard</h1>
            {error && <p style={{ color: 'orange', fontWeight: 'bold' }}>{error}</p>}
            <ul>
                {items.map((item) => <li key={item.id}>{item.title}: {item.content}</li>)}
            </ul>
        </div>
    );
};

export default Dashboard;