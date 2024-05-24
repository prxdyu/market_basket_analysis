# Market Basket Analysis using Apriori

![image](https://miro.medium.com/max/2880/1*DHfQvlMVBaJCHpYmj1kmCw.png)

## 1. Introduction to the Project
Market Basket Analysis is a data mining technique used by retailers to uncover associations between products purchased by customers. It involves analyzing customer purchase patterns to identify relationships between products that are frequently bought together. This analysis helps retailers understand customer behavior, improve product placement strategies, and drive sales by offering targeted promotions and recommendations. 
In this project, the **Apriori algorithm** is employed to  extract meaningful associations from transactional data, aiding in decision-making processes and enhancing market basket analysis strategies.

## 2. Project Structure

```bash
MarketBasketAnalysis
│
├── .github
│   └── workflows
│       └── automate.yml
│
├── MarketBasketAnalysis.egg-info
│
├── artifacts
│   ├── association_rules.pkl
│   └── products.pkl

├── logs
|
├── notebooks
│   └── Training.ipynb
|
├── src
│   ├── components
│   │   ├── data_ingestion.py
│   │   ├── feature_engineer.py
│   │   ├── data_transformation.py
│   │   └── model_trainer.py
│   │
│   ├── exception
│   │   └── logger.py
│   │
│   ├── pipeline
│   │   ├── prediction_pipeline.py
│   │   └── training_pipeline.py
│   │
│   └── utils
│       └── utils.py
│
├── templates
│   ├── form.html
│   ├── index.html
│   └── result.html
│
├── .dockerignore
├── .gitignore
├── Dockerfile
├── app.py
├── init_setup.sh
├── requirements.txt
├── requirements_dev.txt
├── setup.py
└── test.py

```
The project is organized into several components:

- `artifacts` contains association rules pickle file for recommendations.
- `src`: packages the source code for data processing, model training, and evaluation.
- `app.py`: a simple flask application to build API for getting the recommendations.
- `Dockerfile`: defines the Docker image for containerizing the flask application.
- `automate.yml`: configures CI/CD pipelines for automated deployment.

## 3. Src Package and Training/Prediction Pipeline

The src package contains modules for data processing, model training, and evaluation
* **Data Ingestion**: handles data loading and preprocessing.
* **Feature Engineering**: performs feature engineering to create transaction_id
* **Data Transformation**: transforms data for model training.
* **Model Trainer**: trains the machine learning model using preprocessed data.


We have 2 pipelines which are 
- **Training Pipeline**: The training pipeline consists of several steps including Data ingestion, Feature engineering, Data Transformation and Model trainer to train the model
- **Prediction Pipeline**: The prediction pipeline utilizes the trained model to recommend products based on the input basket.

## 4. Flask Application

The Flask application serves as the interface for interacting with the Market Basket Analyzer to get recommendations. It provides endpoints for viewing the home page, testing the server's availability, and making recommendations using the association rules mined by apriori algorithm.

### Endpoints

1. **Home Page** (`/`): Renders the `index.html` template, which provides options for making predictions.
2. **Ping Endpoint** (`/ping`): A simple endpoint for testing the server's availability. Returns "Success" when accessed via a GET request.
3. **Prediction Endpoint** (`/recommend`): Accepts both GET and POST requests. When accessed via GET, it renders a form (`form.html`) populated with options for selecting input features. Upon submitting the form via POST request, it processes the input data, makes predictions using the trained model, and renders the result (`result.html`).

### Input 
Select the products in the basket for which you want to get the recommendations 

### Output

The recommend endpoint displays the recommendation with one or more products for the given basket.

## 5. Dockerfile and Containerization

The Dockerfile provided in the project repository allows for containerizing the  application using a multi-stage build strategy. This strategy helps reduce the size of the final Docker image by separating the build dependencies from the runtime environment.

### Dockerfile Explanation

The Dockerfile consists of two stages:

1. **Builder Stage**: In this stage, a Python 3.8 slim-buster image is used to install the project dependencies specified in the `requirements.txt` file. This stage sets the working directory to `/install` and copies only the `requirements.txt` file to leverage Docker's caching mechanism. It then installs the dependencies into the `/install` directory using `pip`. This stage is responsible for creating a temporary image used for building the dependencies.

2. **Final Stage**: The final Docker image is created based on another Python 3.8 slim-buster image. This stage sets the working directory to `/app` and copies the installed dependencies from the builder stage into the `/usr/local` directory. It then copies the rest of the application files into the `/app` directory. After copying, any unnecessary files are cleaned up to reduce the image size. Finally, the command to run the Flask application is specified using the `CMD` directive, which starts the Flask server on `0.0.0.0:5000`.

### Building the Docker Image

To build the Docker image for the application, navigate to the project directory containing the Dockerfile and execute the following command:

```bash
docker build -t market_basket_analysis .
```

Once the Docker image is built, you can run a Docker container using the following command:
```bash
docker run -d -p 5000:5000 market_basket_analysis
```
This command will start a Docker container based on the  market_basket_analysis image, exposing port 5000 on the host machine. You can then access the Market basket analyzer application by visiting http://localhost:5000 in your web browser


## 6. CI/CD Pipelines

The project utilizes GitHub Actions for Continuous Integration (CI) and Continuous Delivery (CD) pipelines to automate the testing, building, and deployment processes.

![1_jrdZWe4JRU5KDbWfnRxenA](https://github.com/prxdyu/customer_propensity_modelling/assets/105141574/dd8b33fe-5755-498c-83d7-24db2c807857)


### Continuous Integration (CI)

The CI pipeline ensures the correctness and reliability of the application by running automated tests using pytest. These tests validate the functionality of key endpoints in the Flask application. The test.py file is responsible for running the tests to ensure the proper running of flask application

### Continuous Delivery (CD)

The CD pipeline automates the building of the Docker image containing the Flask application and pushes it to the  Amazon ECR.

### Continuous Deployment (CD)

The CD pipeline automates the deployment of the Docker image containing the Flask application by pulling the docker image from the AWS ECR and deploying it to the AWS EC2 instance


#### Test Workflow

- **Workflow Name**: CI/CD Pipeline
- **Trigger**: Automatically triggered upon pushing changes to the `main` branch.
- **Jobs**:
  - **Continous Integration**: runs tests with pytest which tests the flask application when a push is made to the repo.
  - **Continous Delivery**: builds the docker image of the project and pushes it to Amazon ECR.
  - **Continous Deployment**: pulls the docker image of the project from AWS ECR and deploys it to the AWS EC2 instance 


#### Workflow Steps

1. **Checkout**: Checks out the code from the repository.
2. **Install Python 3**: Sets up the Python environment for testing.
3. **Install Dependencies**: Installs project dependencies listed in `requirements_dev.txt`.
4. **Run tests with pytest**: Executes automated tests using pytest.
5. **Print AWS Secrets**: Prints AWS access keys for authentication.
6. **Configure AWS Credentials**: Configures AWS credentials for accessing services.
7. **Login to Amazon ECR**: Logs in to Amazon Elastic Container Registry (ECR) for container image storage.
8. **Build, tag, push image to Amazon ECR**: Builds the Docker image, tags it, and pushes it to Amazon ECR.
9. **Kill containers**: Kills any container which runs on port 5000  
9. **Deploy docker image to EC2 instance**: Pulls the docker image from ECR and Deploys it to an EC2 instance

These CI/CD pipelines ensure the application is thoroughly tested and efficiently deployed to the production environment, enhancing development productivity and maintaining application quality.



