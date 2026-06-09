# Scrapper – Voice Mini AI Assistant

## Description

Scrapper is a small Raspberry Pi based voice assistant prototype designed for simple voice interactions. The device records a user question, processes it using external API services and plays back the generated answer as speech.

The project combines embedded hardware, audio input and output, Python software and AI-based response generation. The software part is responsible for classifying user questions, selecting the correct response mode and communicating with external services such as OpenAI API, weather forecast API and sports data API.

The main goal of the project was to build a working experimental assistant that connects embedded systems, audio processing and API-based artificial intelligence tools.

## Features

* Voice assistant prototype based on Raspberry Pi
* Polish-language response generation
* Question classification into general, sport and weather categories
* General conversation mode using OpenAI API
* Live sports score lookup
* Sports match lookup by date
* Weather forecast retrieval
* Weather description translation to Polish
* Local conversation history with size limiting
* Integration of multiple external API services

## Hardware

* Raspberry Pi
* MEMS microphone
* Speaker
* Custom enclosure
* Audio input and output setup

## Software

* Python
* OpenAI API
* Requests
* OpenWeatherMap API
* RapidAPI sports endpoint
* googletrans
* JSON-based conversation history
* API-based query processing

## System operation

The user asks a question to the assistant. The software first classifies the input into one of three categories:

* `general` – general conversation,
* `sport` – sports results and match information,
* `weather` – weather forecast.

For general questions, the program uses the OpenAI API and a limited local conversation history.

For sports questions, the program detects the sport type, retrieves live or scheduled match data and generates a short answer based on the collected information.

For weather questions, the program retrieves forecast data for a selected city, translates weather descriptions into Polish and generates a response using the available forecast data.

The project was developed as an experimental voice mini assistant and as a practical exercise in combining hardware, audio and AI tools.

## Challenges

Main development challenges:

* handling communication with multiple APIs,
* selecting the correct response mode based on user input,
* processing sports and weather data into short answers,
* managing local conversation history,
* integrating the software with the voice assistant hardware,
* keeping the project usable while protecting API keys and private data.

## Current status

Working prototype built and tested.

## Configuration

API keys are not included in this repository.

##NOTE
The project was designed for my grandfather, so it is set to respond in Polish only.
