import { useState } from "react";
import { FileText, Send, ShieldCheck } from "lucide-react";
import SubmitRequest from "./pages/SubmitRequest.jsx";
import RequestsResponses from "./pages/RequestsResponses.jsx";
import React from "react";

const pages = [
  {
    id: "submit",
    label: "Submit Request",
    icon: Send,
  },
  {
    id: "history",
    label: "User Requests & Responses",
    icon: FileText,
  },
];

export default function App() {
  const [activePage, setActivePage] = useState("submit");

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">
            <ShieldCheck size={26} />
          </div>
          <div>
            <h1>Ticket Sorter</h1>
            <p>Digital finance support classifier</p>
          </div>
        </div>

        <nav className="nav-list">
          {pages.map((page) => {
            const Icon = page.icon;

            return (
              <button
                key={page.id}
                className={`nav-item ${activePage === page.id ? "active" : ""}`}
                onClick={() => setActivePage(page.id)}
              >
                <Icon size={18} />
                <span>{page.label}</span>
              </button>
            );
          })}
        </nav>

        <div className="sidebar-note">
          <strong>Current mode</strong>
          <span>Both pages are visible now. Later you can hide pages based on user role.</span>
        </div>
      </aside>

      <main className="main-content">
        {activePage === "submit" ? <SubmitRequest /> : <RequestsResponses />}
      </main>
    </div>
  );
}
