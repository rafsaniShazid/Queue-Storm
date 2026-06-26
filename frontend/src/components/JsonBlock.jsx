import React from "react";

export default function JsonBlock({ data }) {
  return (
    <pre className="json-block">
      <code>{JSON.stringify(data, null, 2)}</code>
    </pre>
  );
}
