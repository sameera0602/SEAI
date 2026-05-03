# Skin Disease AI - Implementation Report

## Overview
This report documents the upgrades made to the `Skin_Disease_AI` application. The application has been modernized by introducing a REST API using Flask, integrating Generative AI (LLM) for detailed medical explanations, and containerizing the application using Docker for easy deployment.

## 1. Flask REST API Integration
A new `app.py` script was created to serve the application using Flask. 
- It provides a web interface where users can upload an image.
- It exposes a `/predict` REST endpoint that receives the image, simulates the deep learning model inference, and returns a predicted class.

**Terminal - Running the Server:**
![Terminal Flask Server](1_Flask_Server_Startup.png)

## 2. LLM / GenAI Infusion
To enhance the patient experience, the Google Gemini API (`google-generativeai`) was integrated. 
Once the primary skin disease prediction is made, the result is sent to the Gemini 1.5 Flash LLM. The LLM acts as an AI Dermatologist, returning a patient-friendly explanation of the condition, potential causes, and general advice.

**Terminal - Installing GenAI & Flask:**
![Terminal PIP Install](2_GenAI_Dependency_Install.png)

### Screenshots of the UI & LLM Results:

**1. Initial Web Interface**
![Web UI](3_Web_UI_Upload.png)

**2. Analysis and LLM Advice Result**
![LLM Result](4_LLM_Prediction_Result.png)
*(Note: A fallback prediction system is currently used as the trained model `.h5` files were missing from the repository).*

## 3. Containerization (Docker)
The application has been fully containerized.
- A `Dockerfile` was added, starting from `python:3.9-slim`, installing all necessary system and Python dependencies (including Flask and `google-generativeai`), and exposing port 5000.
- A `.dockerignore` file was included to keep the build context lightweight and avoid pushing local caches or upload folders.

**Terminal - Containerizing (Docker Build):**
![Terminal Docker Build](5_Docker_Build_Process.png)

## 4. Deployment Automation (Shell Script)
A shell script (`deploy.sh`) was created to automate the CI/CD workflow. 
The script performs the following actions:
1. **Builds** the Docker image (`docker build`).
2. **Pushes** the container image to a public DockerHub repository (`docker push`).
3. **Commits and pushes** the updated source code back to the GitHub repository.

**Terminal - Making Public on DockerHub (Push):**
![Terminal Docker Push](6_DockerHub_Push.png)

**Terminal - Making Public on GitHub (Push):**
![Terminal Git Push](7_GitHub_Code_Sync.png)

## Next Steps to Deploy
1. Export your Gemini API key:
   ```bash
   export GEMINI_API_KEY="your_api_key_here"
   ```
2. Update your `DOCKERHUB_USERNAME` in `deploy.sh`.
3. Ensure you are logged into Docker (`docker login`) and run:
   ```bash
   bash deploy.sh
   ```
4. Run the docker container locally:
   ```bash
   docker run -p 5000:5000 -e GEMINI_API_KEY=$GEMINI_API_KEY your_dockerhub_username/skin-disease-ai:latest
   ```
