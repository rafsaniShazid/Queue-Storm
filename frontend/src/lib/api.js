const defaultBaseUrl = "http://localhost:8000";

function getApiBaseUrl() {
  return (import.meta.env.VITE_API_BASE_URL || defaultBaseUrl).replace(/\/$/, "");
}

export async function submitTicket(ticket) {
  const response = await fetch(`${getApiBaseUrl()}/sort-ticket`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(ticket),
  });

  const body = await response.json().catch(() => null);

  if (!response.ok) {
    const detail = body?.detail || "Ticket classification failed";
    throw new Error(detail);
  }

  return body;
}