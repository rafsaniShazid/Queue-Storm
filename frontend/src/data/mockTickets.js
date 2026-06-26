export const mockTickets = [
  {
    request: {
      ticket_id: "T-001",
      channel: "app",
      locale: "en",
      message: "I sent 5000 taka to a wrong number this morning, please help me get it back",
    },
    response: {
      ticket_id: "T-001",
      case_type: "wrong_transfer",
      severity: "high",
      department: "dispute_resolution",
      agent_summary: "Customer reports sending 5000 BDT to a wrong number and requests recovery.",
      human_review_required: true,
      confidence: 0.85,
    },
  },
  {
    request: {
      ticket_id: "T-002",
      channel: "sms",
      locale: "mixed",
      message: "Amar payment ta fail hoise but account theke taka kete niyeche.",
    },
    response: {
      ticket_id: "T-002",
      case_type: "failed_payment",
      severity: "medium",
      department: "payments",
      agent_summary: "Customer says a payment failed but money was deducted from the account.",
      human_review_required: false,
      confidence: 0.79,
    },
  },
  {
    request: {
      ticket_id: "T-003",
      channel: "call_center",
      locale: "en",
      message: "Someone called me and asked for my OTP and PIN saying they are from support.",
    },
    response: {
      ticket_id: "T-003",
      case_type: "phishing",
      severity: "critical",
      department: "fraud",
      agent_summary: "Customer reports a suspicious caller asking for OTP and PIN.",
      human_review_required: true,
      confidence: 0.94,
    },
  },
  {
    request: {
      ticket_id: "T-004",
      channel: "merchant_portal",
      locale: "en",
      message: "Customer wants refund for a duplicate merchant charge from yesterday.",
    },
    response: {
      ticket_id: "T-004",
      case_type: "refund",
      severity: "medium",
      department: "customer_support",
      agent_summary: "Customer requests a refund for a duplicate merchant charge.",
      human_review_required: false,
      confidence: 0.82,
    },
  },
];
