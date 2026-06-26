import React from "react";
import { AlertTriangle, FileJson, ShieldAlert } from "lucide-react";
import JsonBlock from "../components/JsonBlock.jsx";
import StatusBadge from "../components/StatusBadge.jsx";
import { mockTickets } from "../data/mockTickets.js";

export default function RequestsResponses() {
  const total = mockTickets.length;
  const reviewCount = mockTickets.filter((item) => item.response.human_review_required).length;
  const criticalCount = mockTickets.filter((item) => item.response.severity === "critical").length;

  return (
    <section className="page">
      <div className="page-header">
        <div>
          <p className="eyebrow">Second page</p>
          <h2>User Requests & Responses</h2>
          <p>
            Hard-coded examples of incoming CRM ticket requests and structured classification responses.
          </p>
        </div>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <span>Total Tickets</span>
          <strong>{total}</strong>
        </div>

        <div className="stat-card">
          <span>Human Review</span>
          <strong>{reviewCount}</strong>
        </div>

        <div className="stat-card danger">
          <span>Critical Cases</span>
          <strong>{criticalCount}</strong>
        </div>
      </div>

      <div className="ticket-list">
        {mockTickets.map((item) => (
          <article className="ticket-card" key={item.request.ticket_id}>
            <div className="ticket-top">
              <div>
                <div className="ticket-id">
                  <FileJson size={18} />
                  <strong>{item.request.ticket_id}</strong>
                </div>
                <p>{item.request.message}</p>
              </div>

              {item.response.human_review_required && (
                <div className="human-review-tag">
                  <ShieldAlert size={17} />
                  Human review
                </div>
              )}
            </div>

            <div className="classification-row">
              <div>
                <span>Case Type</span>
                <strong>{item.response.case_type}</strong>
              </div>

              <div>
                <span>Severity</span>
                <StatusBadge type="severity">{item.response.severity}</StatusBadge>
              </div>

              <div>
                <span>Department</span>
                <strong>{item.response.department}</strong>
              </div>

              <div>
                <span>Confidence</span>
                <strong>{Math.round(item.response.confidence * 100)}%</strong>
              </div>
            </div>

            <div className="summary-box">
              <strong>Agent Summary</strong>
              <p>{item.response.agent_summary}</p>
            </div>

            {item.response.human_review_required && (
              <div className="review-alert compact">
                <AlertTriangle size={18} />
                <span>This ticket should be reviewed quickly by a human agent.</span>
              </div>
            )}

            <div className="json-columns">
              <div>
                <h4>Request JSON</h4>
                <JsonBlock data={item.request} />
              </div>

              <div>
                <h4>Response JSON</h4>
                <JsonBlock data={item.response} />
              </div>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
