# Tool-Calling Chatbot Project

## Overview

Build a chatbot using OpenAI's API that calls three different tools (functions) in response to a user prompt. The tools return simulated or "fake" information and do not need to provide real data.

## Objective

Create a functional chatbot that demonstrates tool-calling capabilities using OpenAI's API, implementing three distinct tools for weather reporting, currency conversion, and language translation.

## Tools Implementation

### 1. Weather Check Tool

A tool that simulates weather reporting for any given location.

**Specifications:**

-   **Input:** location
-   **Output:** Fake weather information
    -   Temperature
    -   Weather description

### 2. Currency Conversion Tool

A tool that simulates currency conversion between two different currencies.

**Specifications:**

-   **Input:**
    -   Amount
    -   From currency
    -   To currency
-   **Output:** Fabricated conversion amount

### 3. Language Translation Tool

A tool that simulates text translation into specified languages.

**Specifications:**

-   **Input:**
    -   Text
    -   Target language
-   **Output:** Simulated translation

## Notes

-   All tools return simulated data
-   No need for real API integrations for weather, currency, or translation services
-   Focus is on implementing the tool-calling structure using OpenAI's API
