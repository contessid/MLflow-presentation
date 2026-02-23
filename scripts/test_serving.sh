#!/usr/bin/env bash
# Test the MLflow model serving endpoint

echo "=== Testing temperature forecast model ==="
echo ""
echo "Requesting 30-day forecast..."
echo ""

curl -s http://localhost:5001/invocations \
  -H "Content-Type: application/json" \
  -d '{"dataframe_split": {"columns": ["n_steps"], "data": [[30]]}}' | python3 -m json.tool

echo ""
echo "=== Done ==="
