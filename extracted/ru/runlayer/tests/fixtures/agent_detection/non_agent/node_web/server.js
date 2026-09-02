// Plain Express web service — not an AI agent (zero-false-positive fixture).
import express from "express";

const app = express();
app.use(express.json());

const items = [];

app.get("/health", (req, res) => {
  res.json({ status: "ok" });
});

app.post("/items", (req, res) => {
  const item = { id: items.length + 1, ...req.body };
  items.push(item);
  res.status(201).json(item);
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`listening on ${port}`);
});
