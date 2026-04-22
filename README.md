# LogiSense AI — Resilient Logistics and Dynamic Supply Chain Optimization

> Google Solution Challenge 2026 | Smart Supply Chains Track

![Status](https://img.shields.io/badge/Status-Live-brightgreen)
![GCP](https://img.shields.io/badge/Google%20Cloud-Deployed-blue)
![Gemini](https://img.shields.io/badge/Gemini%20AI-Powered-orange)
![Cost](https://img.shields.io/badge/Cost-Free%20Tier-success)

## Live Demo

Dashboard: https://logisense-dashboard-924607236415.us-central1.run.app

---

## Problem Statement

Modern global supply chains manage millions of concurrent shipments across
highly complex and volatile transportation networks. Critical transit
disruptions from sudden weather events, port congestion, and carrier failures
are identified only AFTER delivery timelines are already compromised.

The result: Billions in losses. Zero warning. No time to react.

---

## Our Solution

LogiSense AI is a real-time supply chain disruption detection and intelligent
rerouting platform built entirely on Google Cloud free tier.

It continuously ingests live shipment telemetry, weather feeds, and port
status data then uses Gemini AI to analyze multi-factor risk patterns and
proactively recommend optimized alternate routes BEFORE delays cascade.

Reaction time reduced from hours to seconds.

---

## Architecture Diagram

    +---------------------------+
    |   Shipment Events         |
    |   IoT Sensors and APIs    |
    +---------------------------+
                 |
                 v
    +---------------------------+
    |   Cloud Pub/Sub           |
    |   Topic: shipment-events  |
    +---------------------------+
                 |
                 v
    +---------------------------+
    |   Cloud Functions Gen2    |
    |   Trigger: Pub/Sub event  |
    +---------------------------+
                 |
                 v
    +---------------------------+
    |   Gemini AI via Vertex AI |
    |                           |
    |   Analyze weather data    |
    |   Score port congestion   |
    |   Assess carrier delays   |
    |   Generate risk score     |
    |   Recommend rerouting     |
    +---------------------------+
                 |
                 v
    +---------------------------+
    |   Cloud Firestore         |
    |   Collection: shipments   |
    +---------------------------+
                 |
                 v
    +---------------------------+
    |   Cloud Run Dashboard     |
    |   Live shipment table     |
    |   Color coded risk scores |
    |   AI recommendations      |
    |   Auto refresh every 20s  |
    +---------------------------+

---

## CI/CD Pipeline Diagram

    Developer pushes code to GitHub
                 |
                 v
    +---------------------------+
    |   GitHub Repository       |
    |   Branch: main            |
    +---------------------------+
                 |
                 v  webhook trigger
    +---------------------------+
    |   Cloud Build             |
    |   cloudbuild.yaml         |
    |                           |
    |   Step 1: Build Docker    |
    |   Step 2: Push to Registry|
    |   Step 3: Deploy Cloud Run|
    +---------------------------+
                 |
                 v
    +---------------------------+
    |   Cloud Run               |
    |   Live update in 3 mins   |
    +---------------------------+

---

## Risk Level System

    +----------+----------+----------------------------------+
    |  Score   |  Level   |  Action                          |
    +----------+----------+----------------------------------+
    |  0 - 40  |  LOW     |  Standard monitoring             |
    | 41 - 70  |  MEDIUM  |  Prepare contingency route       |
    | 71 - 100 |  HIGH    |  Immediate rerouting required    |
    +----------+----------+----------------------------------+

---

## Google Cloud Services Used

    +------------------------+------------------------------------------+
    |  Service               |  Purpose                                 |
    +------------------------+------------------------------------------+
    |  Gemini AI Vertex AI   |  Risk analysis and rerouting logic       |
    |  Cloud Run             |  Hosts the live dashboard                |
    |  Cloud Firestore       |  Real-time shipment data storage         |
    |  Cloud Pub/Sub         |  Event streaming for shipment telemetry  |
    |  Cloud Functions       |  Serverless event processor              |
    |  Cloud Build           |  CI/CD pipeline auto-deployment          |
    |  Artifact Registry     |  Docker image storage                    |
    +------------------------+------------------------------------------+

---

## Key Features

- Real-time disruption detection across weather, port, and carrier data
- Gemini AI powered multi-factor risk scoring from 0 to 100
- Proactive rerouting recommendations before ETA is missed
- Natural language AI explanations for every risk flag
- Live auto-refreshing dashboard showing all active shipments
- Event-driven serverless architecture via Cloud Pub/Sub
- Full CI/CD pipeline — GitHub push auto-deploys to Cloud Run
- Zero infrastructure cost — 100% Google Cloud free tier

---

## Project Structure

    logisense-ai/
    |
    |-- dashboard/
    |   |-- app.py              Flask dashboard application
    |   |-- Dockerfile          Container config Python 3.11
    |   |-- requirements.txt    Flask Firestore Gunicorn
    |
    |-- functions/
    |   |-- main.py             Cloud Function with Gemini AI
    |   |-- requirements.txt    Vertex AI Firestore deps
    |
    |-- analyze.py              Local Gemini analyzer script
    |-- cloudbuild.yaml         CI/CD pipeline configuration
    |-- README.md               This file

---

## How It Works Step by Step

    Step 1  Shipment event published to Cloud Pub/Sub
                 |
    Step 2  Cloud Function triggers automatically
                 |
    Step 3  Gemini AI analyzes these factors
            - Weather severity at origin port
            - Port congestion score 0 to 1
            - Carrier delay in hours
            - Combined multi-factor risk
                 |
    Step 4  Risk score 0 to 100 generated with plain English explanation
                 |
    Step 5  Rerouting recommendation saved to Firestore
                 |
    Step 6  Dashboard auto-refreshes showing live results

---

## Free Tier Cost Breakdown

    +---------------------+----------------------+----------+
    |  Service            |  Usage               |  Cost    |
    +---------------------+----------------------+----------+
    |  Cloud Run          |  Under 2M requests   |  $0      |
    |  Cloud Firestore    |  Under 1GB storage   |  $0      |
    |  Cloud Pub/Sub      |  Under 10GB/month    |  $0      |
    |  Cloud Functions    |  Under 2M calls      |  $0      |
    |  Cloud Build        |  Under 120 min/day   |  $0      |
    |  Gemini AI          |  Free tier quota     |  $0      |
    +---------------------+----------------------+----------+
    |  TOTAL              |                      |  $0/mo   |
    +---------------------+----------------------+----------+

---

## Team Details

- Team Name: LogiSense AI
- Problem Statement: Smart Supply Chains — Resilient Logistics and Dynamic Supply Chain Optimization
- Event: Google Solution Challenge 2026
- Google AI Used: Gemini AI via Vertex AI
- Deployed on Google Cloud: Yes

---

## Submission Links

- Live Dashboard: https://logisense-dashboard-924607236415.us-central1.run.app
- GitHub Repository: https://github.com/Yogendra1823/logisense-ai
- Solution Challenge: https://developers.google.com/community/gdsc-solution-challenge

# Updated Wed Apr 22 04:44:32 AM UTC 2026
