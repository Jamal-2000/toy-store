#  Toy Store --- Flask + Cloud Run CI/CD

This project is a fully containerized Flask e-commerce application
deployed on **Google Cloud Run** using **Cloud Build CI/CD**.

------------------------------------------------------------------------

## 📦 Features

-   Flask backend
-   Product catalog pages (Home, Products, Product Details)
-   Static asset hosting
-   Dockerized application
-   CI/CD using Cloud Build
-   Automatic Cloud Run deployment
-   GitHub-trigger integration

------------------------------------------------------------------------

## 🏗️ Architecture Diagram

See `architecture.png`

------------------------------------------------------------------------

## 🔧 Technologies Used

-   **Python + Flask**
-   **Docker**
-   **Google Cloud Run**
-   **Google Cloud Build**
-   **Artifact Registry**
-   **GitHub Integration**

------------------------------------------------------------------------

## 🚀 Deployment Pipeline

1.  Push code to GitHub `main` branch.
2.  Cloud Build trigger activates.
3.  Cloud Build runs:
    -   Docker build
    -   Docker push
    -   Cloud Run deployment
4.  Cloud Run serves latest version automatically.

------------------------------------------------------------------------

## 📁 Important Files

-   `cloudbuild.yaml`\
-   `Dockerfile`\
-   `main.py`\
-   `/templates`\
-   `/static`

------------------------------------------------------------------------


