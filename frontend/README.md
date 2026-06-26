# Ticket Sorter UI

React/Vite UI for a digital finance CRM ticket classification service.

## Pages

1. **Submit Request**  
   Form for submitting one CRM ticket and calling the FastAPI backend.

2. **User Requests & Responses**  
   Shows hard-coded ticket requests and classification responses.

The UI calls `POST /sort-ticket` on the backend. Set `VITE_API_BASE_URL` if the API is not running on `http://localhost:8000`.

When running with Docker Compose from the repo root, put `GEMINI_API_KEY` in the root `.env` file.

---

## Run with Docker

From the repository root:

```bash
docker compose up --build
```

Then open:

```text
http://localhost:5174
```

---

## Stop Docker

Press:

```bash
CTRL + C
```

Then run:

```bash
docker compose down
```

---

## Refresh after changing code

You usually do **not** need to restart Docker.

Just save the file. Vite should auto-refresh the browser.

If it still does not refresh, hard refresh the browser:

```text
CTRL + F5
```

If Docker gets stuck, restart:

```bash
docker compose down
docker compose up --build
```

If you want a different port, set `FRONTEND_PORT` in the repo-root `.env` file.

---

## Where to add backend API later

Open:

```text
src/pages/SubmitRequest.jsx
```

Inside `handleSubmit`, you will find the backend API call commented out.

Example:

```js
// const response = await fetch("http://localhost:8000/sort-ticket", {
//   method: "POST",
//   headers: { "Content-Type": "application/json" },
//   body: JSON.stringify(payload),
// });
// const data = await response.json();
```
