# Research Fetcher — 2026-04-01

Raw output from the research-fetcher cron job.

---

34 insights found:

1. "Use retrieval over raw parametric recall to ground knowledge-heavy answers, and keep the backing memory human-readable and editable." — from Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks
2. "Let the model decide when to retrieve, generate, or critique itself instead of forcing fixed retrieval everywhere." — from Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection
3. "Chain retrieval and evidence accumulation across steps to improve robustness on retrieval-augmented tasks." — from Chain-of-Note: Enhancing Robustness in Retrieval-Augmented Language Models
4. "RAG needs tight evaluation across retriever, generator, and grounding quality, not just end-answer accuracy." — from A Survey on RAG Meeting LLMs: Towards Retrieval-Augmented Large Language Models
5. "Reasoning quality can improve when the model explores alternative decoding paths rather than only the greedy one." — from Chain-of-Thought Reasoning without Prompting
6. "Replace expensive cost-volume matching with simpler warping to get faster stereo matching without losing accuracy." — from WAFT-Stereo: Warping-Alone Field Transforms for Stereo Matching
7. "Autonomous coding agents can serve as variation operators in evolutionary search, replacing hand-designed mutation and crossover." — from AVO: Agentic Variation Operators for Autonomous Evolutionary Search
8. "Pure reinforcement learning can bootstrap strong reasoning behavior without relying on human-annotated chains of thought." — from DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning
9. "Memory systems for agents should dynamically organize and revise memories, not just store and retrieve them flatly." — from A-Mem: Agentic Memory for LLM Agents
10. "For uncertain tasks, training models to produce multiple plausible answers improves calibration and diversity instead of collapsing to one mode." — from Reaching Beyond the Mode: RL for Distributional Reasoning in Language Models
11. "Behavioral safety must be checked during execution, not only at final outcome, because agents can violate constraints mid-trajectory." — from BeSafe-Bench: Unveiling Behavioral Safety Risks of Situated Agents in Functional Environments
12. "LLM-driven simulation workflows work better when generation, execution, evaluation, and feedback are separated into explicit stages." — from AutoB2G: A Large Language Model-Driven Agentic Framework For Automated Building-Grid Co-Simulation
13. "Short-video training can still support long-video inference if the KV cache is partitioned and managed carefully." — from PackForcing: Short Video Training Suffices for Long Video Sampling and Long Context Inference
14. "Local trajectory lessons can be distilled into reusable skills, and parallel consolidation avoids sequential drift." — from Trace2Skill: Distill Trajectory-Local Lessons into Transferable Agent Skills
15. "Real-world chart-to-code needs both generation and refinement tasks, because chart making fails in layout, mapping, and scaling in specific ways." — from RealChart2Code: Advancing Chart-to-Code Generation with Real Data and Multi-Task Evaluation
16. "Agent harness behavior should be externalized into portable, editable natural language so control logic is easier to compare and reuse." — from Natural-Language Agent Harnesses
17. "Repository memory should capture organic project patterns, not just the current code snapshot, to produce maintainable pull requests." — from Learning to Commit: Generating Organic Pull Requests via Online Repository Memory
18. "Software agents improve when the training harness closely matches the real deployment harness and tool semantics." — from Composer 2 Technical Report
19. "Chain-of-thought is not always faithful, so verbal reasoning cannot be assumed to reflect the true causes of a model output." — from Lie to Me: How Faithful Is Chain-of-Thought Reasoning in Reasoning Models?
20. "Bitboard-style state compression and bitwise operations can make a game AI much faster and more scalable." — from Bitboard version of Tetris AI
21. "Shared representations can let a text-to-level generator blend concepts across multiple game domains." — from Multiverse: Language-Conditioned Multi-Game Level Blending via Shared Representation
22. "A structured writing scaffold with persistent visual contracts improves scientific paper coherence and alignment between text and figures." — from Story2Proposal: A Scaffold for Structured Scientific Paper Writing
23. "Adaptive compression should respond to information density instead of using one fixed context reduction ratio everywhere." — from Density-aware Soft Context Compression with Semi-Dynamic Compression Ratio
24. "Number-free motion generation becomes more robust when one model handles prior motion and reaction stages in a unified latent space." — from Unified Number-Free Text-to-Motion Generation Via Flow Matching
25. "Specializing different expert domains and then unifying them can improve agentic coding performance at scale." — from KAT-Coder-V2 Technical Report
26. "Very long-term conversational memory needs explicit evaluation because ordinary long-context tests miss multi-session failures." — from Evaluating Very Long-Term Conversational Memory of LLM Agents
27. "Entropy can act as a global uncertainty signal for token selection and early stopping in long-video understanding." — from AdaptToken: Entropy-based Adaptive Token Selection for MLLM Long Video Understanding
28. "Large-scale bimanual motion generation depends on high-fidelity paired data and supports both diffusion and autoregressive models." — from HandX: Scaling Bimanual Motion and Interaction Generation
29. "Training-free in-context segmentation is possible directly from strong pretrained features, with no decoder fine-tuning." — from INSID3: Training-Free In-Context Segmentation with DINOv3
30. "Streaming video understanding works better when the model learns when to speak, not only what to say." — from STRIDE: When to Speak Meets Sequence Denoising for Streaming Video Understanding
31. "Pure RL can also drive stronger reasoning in open reasoning models without supervised reasoning traces." — from DeepSeek-R1 incentivizes reasoning in LLMs through reinforcement learning
32. "ARC-AGI-2 shows that benchmark tasks need to probe general problem solving, not just domain knowledge or routine pattern matching." — from ARC-AGI-2: A New Challenge for Frontier AI Reasoning Systems
33. "Comparing chart pairs is a distinct task from single-chart reading, and needs benchmarked cross-chart summarization." — from ChartDiff: A Large-Scale Benchmark for Comprehending Pairs of Charts
34. "A formal comparative framework can help organize and analyze AGI architectures rather than treating them as ad hoc systems." — from Working Paper: Towards a Category-theoretic Comparative Framework for Artificial General Intelligence
35. "Photorealistic face synthesis improves when semantic and structural modalities are processed in separate streams and fused in diffusion." — from MMFace-DiT: A Dual-Stream Diffusion Transformer for High-Fidelity Multimodal Face Generation
36. "Scientific idea generation can be improved by guided literature exploration and iterative evolution at test time." — from FlowPIE: Test-Time Scientific Idea Evolution with Flow-Guided Literature Exploration

---

## Proposed Actions

1. **AGENTS.md → Response Defaults + Named Agent Delegation**: Add rule that retrieval-heavy answers should separate evidence from inference, and delegate long synthesis-heavy research writeups to a drafting agent. *Reasoning: several papers point to retrieval quality, evidence accumulation, and harness design as first-class control problems.* **→ APPROVED & APPLIED**

2. **AGENTS.md → Security Protocols**: Add explicit reminder that chain-of-thought or internal reasoning should not be treated as faithful evidence unless corroborated. *Reasoning: the faithfulness paper argues reasoning traces can diverge from actual causes.* **→ APPROVED & APPLIED**

3. **AGENTS.md → Memory Management**: Add rule to store durable skills as structured memory only after repeated validation, with separate entries for workflow habits, project-specific conventions, and uncertainty/safety notes. *Reasoning: agent memory and repository-memory papers both emphasize dynamic, organized memory rather than flat logs.* **→ APPROVED & APPLIED**

4. **MEMORY.md → Patterns + Open Loops**: Add validated preference to keep answers short, evidence-linked, and split into "what the source says" versus "what I infer" when using recent research. *Reasoning: the new corpus strongly rewards explicit evidence handling and concise, structured reporting.* **→ APPROVED & APPLIED**
