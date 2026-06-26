import React from "react";
import { useMemo, useState } from "react";
import { AlertTriangle, CheckCircle2, Copy, LoaderCircle, RotateCcw, Send } from "lucide-react";
import JsonBlock from "../components/JsonBlock.jsx";
import { submitTicket } from "../lib/api.js";

const initialForm = {
  ticket_id: "T-005",
  channel: "app",
  locale: "en",
  message: "I sent 5000 taka to a wrong number this morning, please help me get it back",
};

export default function SubmitRequest() {
  const [form, setForm] = useState(initialForm);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [copied, setCopied] = useState(false);

  const payload = useMemo(
    () => ({
      ticket_id: form.ticket_id.trim(),
      channel: form.channel,
      locale: form.locale,
      message: form.message.trim(),
    }),
    [form]
  );

  const isValid = payload.ticket_id && payload.message;

  const handleChange = (event) => {
    const { name, value } = event.target;

    setForm((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!isValid) return;

    setError("");
    setIsSubmitting(true);

    try {
      const data = await submitTicket(payload);
      setResult(data);
    } catch (submitError) {
      setError(submitError instanceof Error ? submitError.message : "Backend request failed");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleReset = () => {
    setForm(initialForm);
    setResult(null);
    setError("");
    setCopied(false);
    setIsSubmitting(false);
  };

  const copyJson = async () => {
    const text = JSON.stringify(result || payload, null, 2);
    await navigator.clipboard.writeText(text);
    setCopied(true);

    setTimeout(() => setCopied(false), 1500);
  };

  return (
    <section className="page">
      <div className="page-header">
        <div>
          <p className="eyebrow">First page</p>
          <h2>Submit Request</h2>
          <p>
            Submit one CRM ticket and get a structured classification response from the FastAPI backend.
          </p>
        </div>

        <div className="health-pill">
          <CheckCircle2 size={18} />
          <span>Backend Connected</span>
        </div>
      </div>

      <div className="submit-grid">
        <form className="card form-card" onSubmit={handleSubmit}>
          <div className="card-heading">
            <h3>Ticket Input</h3>
            <p>Required fields: ticket_id and message.</p>
          </div>

          <div className="form-row two-columns">
            <label>
              Ticket ID
              <input
                name="ticket_id"
                value={form.ticket_id}
                onChange={handleChange}
                placeholder="T-001"
              />
            </label>

            <label>
              Channel
              <select name="channel" value={form.channel} onChange={handleChange}>
                <option value="app">app</option>
                <option value="sms">sms</option>
                <option value="call_center">call_center</option>
                <option value="merchant_portal">merchant_portal</option>
              </select>
            </label>
          </div>

          <div className="form-row">
            <label>
              Locale
              <select name="locale" value={form.locale} onChange={handleChange}>
                <option value="en">en</option>
                <option value="bn">bn</option>
                <option value="mixed">mixed</option>
              </select>
            </label>
          </div>

          <div className="form-row">
            <label>
              Customer Message
              <textarea
                name="message"
                value={form.message}
                onChange={handleChange}
                placeholder="Write customer complaint here..."
                rows={8}
              />
            </label>
          </div>

          {!isValid && (
            <div className="warning-box">
              <AlertTriangle size={18} />
              <span>Ticket ID and message are required.</span>
            </div>
          )}

          <div className="button-row">
            <button className="primary-button" type="submit" disabled={!isValid || isSubmitting}>
              {isSubmitting ? <LoaderCircle size={18} className="spin" /> : <Send size={18} />}
              {isSubmitting ? "Submitting..." : "Submit Request"}
            </button>

            <button className="secondary-button" type="button" onClick={handleReset}>
              <RotateCcw size={18} />
              Reset
            </button>
          </div>
        </form>

        <div className="card preview-card">
          <div className="card-heading with-action">
            <div>
              <h3>{result ? "Mock Response JSON" : "Request JSON Preview"}</h3>
              <p>{result ? "This simulates POST /sort-ticket response." : "This is the payload to send."}</p>
            </div>

            <button className="icon-button" onClick={copyJson} type="button">
              <Copy size={17} />
              {copied ? "Copied" : "Copy"}
            </button>
          </div>

          {error && (
            <div className="warning-box backend-warning">
              <AlertTriangle size={18} />
              <span>{error}. Check that the FastAPI server is running on the configured base URL.</span>
            </div>
          )}

          <JsonBlock data={result || payload} />

          {result?.human_review_required && (
            <div className="review-alert">
              <AlertTriangle size={19} />
              <div>
                <strong>Human review required</strong>
                <span>Triggered because severity is critical/high or case looks sensitive.</span>
              </div>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
