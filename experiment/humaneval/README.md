## run inference
```shell
python -m experiment.humaneval.inference \
  --data_name openai/openai_humaneval \
  --split test \
  --output_file experiment/interpreter_predictions.jsonl \
  --on_hexel \
#  --max_num 1 \
  --agent_type interpreter \
  --llm_name gpt-4o-mini \
  --max_new_tokens 8000
```
