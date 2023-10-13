# Backend Information

## Table of Contents

1. [Description](#description)
2. [Features](#features)
3. [Technologies](#technologies)
4. [Deployment](#deployment)
5. [Usage](#usage)
6. [Rate Limiting](#rate-limiting)

## Description

This repository hosts the backend logic for the ThreadMind platform, specialized in analyzing YouTube and Reddit comments. It leverages various machine learning models and techniques to calculate sentiment, emotion, and cyberbullying levels, along with comment summarization and keyword extraction.

## Features

- **Data Fetching**: Fetches post/video descriptions, channel/subreddit descriptions, statistics, and comments by interacting with YouTube and Reddit APIs.
  
- **Comment Analysis**: Provides functionalities for sentiment analysis, text emotion recognition, and cyberbullying classification.
  
- **Text Summarization**: Utilizes OpenAI GPT-3.5TURBO for comment summarization and keyword extraction.

## Technologies

- REST API for frontend-backend communication
- Deployed on Heroku
- YouTube API and Reddit API for data fetching
- OpenAI GPT-3.5TURBO for text summarization
- Google Cloud Run for hosting fine-tuned machine learning models

## Deployment

The backend is deployed on Heroku. Follow the official [Heroku documentation](https://devcenter.heroku.com/) to deploy your own instance.

## Usage

For detailed usage instructions, click on the [link](https://thread-mind.vercel.app/) provided in the repository description.


## Rate Limiting

Rate-limiting logic is applied to control the number of requests. A session ID is also generated to prevent duplicate requests.
