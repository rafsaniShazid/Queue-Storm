import React from "react";

const severityClass = {
  low: "badge-low",
  medium: "badge-medium",
  high: "badge-high",
  critical: "badge-critical",
};

export default function StatusBadge({ type = "default", children }) {
  const className = type === "severity" ? severityClass[String(children).toLowerCase()] : "";

  return <span className={`status-badge ${className}`}>{children}</span>;
}
