import { useEffect, useState } from "react";
import type { FormEvent } from "react";
import { createPrompt, getPrompts } from "../services/promptService";
import type {
  Prompt,
  PromptServiceError,
  ValidationError,
} from "../services/promptService";
import "./Dashboard.css";

const Dashboard = () => {
  const [items, setItems] = useState<Prompt[]>([]);
  const [errorMessage, setErrorMessage] = useState("");
  const [success, setSuccess] = useState("");
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [validationErrors, setValidationErrors] = useState<ValidationError>({});
  const [isLoading, setIsLoading] = useState(false);

  const fetchPrompts = async () => {
    try {
      const response = await getPrompts();
      setItems(response);
      setErrorMessage("");
    } catch (error) {
      const serviceError = error as PromptServiceError;
      setErrorMessage(serviceError.message);
    }
  };

  useEffect(() => {
    fetchPrompts();
  }, []);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setErrorMessage("");
    setSuccess("");
    setValidationErrors({});

    try {
      await createPrompt({ title, content });
      setSuccess("Prompt was added successfully.");
      setTitle("");
      setContent("");
      await fetchPrompts();
    } catch (error) {
      const serviceError = error as PromptServiceError;
      setErrorMessage(serviceError.message);

      if (serviceError.status === 400 && serviceError.validationErrors) {
        setValidationErrors(serviceError.validationErrors);
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="dashboard">
      <header className="dashboard__header">
        <h1 className="dashboard__title">PromptVault Dashboard</h1>
        <p className="dashboard__subtitle">
          Create and browse prompts in one place.
        </p>
      </header>

      <section className="panel">
        <h2 className="panel__title">Add a new prompt</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label" htmlFor="prompt-title">
              Title
            </label>
            <input
              id="prompt-title"
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className={`input ${validationErrors.title ? "input--error" : ""}`}
              placeholder="e.g. Prompt for code review"
            />
            {validationErrors.title && (
              <p className="field-error" role="alert">
                {validationErrors.title.join(", ")}
              </p>
            )}
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="prompt-content">
              Content
            </label>
            <textarea
              id="prompt-content"
              value={content}
              onChange={(e) => setContent(e.target.value)}
              rows={5}
              className={`input input--textarea ${validationErrors.content ? "input--error" : ""}`}
              placeholder="Prompt content..."
            />
            {validationErrors.content && (
              <p className="field-error" role="alert">
                {validationErrors.content.join(", ")}
              </p>
            )}
          </div>

          <button type="submit" disabled={isLoading} className="button-primary">
            {isLoading ? "Sending..." : "Add prompt"}
          </button>
        </form>

        {success && (
          <p className="notice notice--success" role="status">
            {success}
          </p>
        )}
      </section>

      {errorMessage && (
        <div className="notice notice--error" role="alert">
          {errorMessage}
        </div>
      )}

      <section className="panel">
        <h2 className="panel__title">Prompt list ({items.length})</h2>
        {items.length === 0 ? (
          <p className="empty-state">
            No prompts yet. Add the first prompt using the form above.
          </p>
        ) : (
          <div className="prompt-grid">
            {items.map((item) => (
              <article key={item.id} className="prompt-card">
                <h3 className="prompt-card__title">{item.title}</h3>
                <p className="prompt-card__content">{item.content}</p>
                <div className="prompt-card__meta">ID: {item.id}</div>
              </article>
            ))}
          </div>
        )}
      </section>
    </main>
  );
};

export default Dashboard;
