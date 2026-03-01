# Real-Time Banking Customer Intent Triage System

## Overview

This project implements a production-oriented AI banking intent detection and risk-aware triage system.

Instead of using a flat fine-tuned classifier, the system adopts a hybrid retrieval + transformer-based re-ranking architecture to improve scalability, interpretability, and open-set robustness.

## Architecture

The system consists of:

1. Semantic Retrieval (FAISS + Sentence Embeddings)
2. Cross-Encoder Re-Ranking
3. Risk Classification Engine
4. Decision Policy Layer (AI-first / Human Escalation)
5. AI Monitoring Dashboard (Frontend)

## Risk-Based Handling

Intents are categorized into:

- LOW_RISK → AI Self-Service
- HIGH_RISK → AI Triage then Human
- CRITICAL → Immediate Human Escalation
- OUT_OF_DOMAIN → Safe Rejection

## Key Features

- Real-time intent detection
- Open-set query rejection
- Risk-aware decision engine
- Human-in-the-loop escalation
- Monitoring dashboard with live metrics
- Modular and scalable architecture

## Tech Stack

Backend:
- FastAPI
- FAISS
- Sentence Transformers
- Cross-Encoder (MiniLM)

Frontend:
- React + Vite
- AI Monitoring Dashboard

## Example Flow

User Query:
> "I lost my credit card"

System Response:
- Intent: lost_or_stolen_card
- Risk: CRITICAL
- Handling: Immediate Human Escalation

## Motivation

Designed to demonstrate production-grade AI system design principles including modular architecture, explainability, risk modeling, and scalable intent handling for digital banking environments.
