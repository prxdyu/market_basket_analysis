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

- **artifacts**: contains association rules pickle file for recommendations.
- **src**: packages the source code for data processing, model training, and evaluation.
- **app.py**: a simple flask application to build API for getting the recommendations.
- **Dockerfile**: defines the Docker image for containerizing the flask application.
- **automate.yml**: configures CI/CD pipelines for automated deployment.

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
3. **Prediction Endpoint** (`/predict`): Accepts both GET and POST requests. When accessed via GET, it renders a form (`form.html`) populated with options for selecting input features. Upon submitting the form via POST request, it processes the input data, makes predictions using the trained model, and renders the result (`result.html`).

### Input Features

The prediction endpoint accepts the following input features:

- **Category**: The category of the product.
- **Subcategory**: The subcategory of the product.
- **Days Active**: Number of days the user has been active.
- **R**: Recency (a measure of how recently the user made a purchase).
- **F**: Frequency (a measure of how often the user makes purchases).
- **M**: Monetary value (a measure of how much money the user spends).
- **Loyalty**: Loyalty status of the user.
- **Avg Purchase Gap**: Average time gap between purchases.
- **Add to Cart to Purchase Ratios**: Ratio of add-to-cart actions to purchases.
- **Add to Wishlist to Purchase Ratios**: Ratio of add-to-wishlist actions to purchases.
- **Click Wishlist Page to Purchase Ratios**: Ratio of clicks on wishlist page to purchases.
- **User Path**: Path followed by the user on the website.
- **Cart to Purchase Ratios (Category and Subcategory)**: Ratios of cart actions to purchases for both category and subcategory.
- **Wishlist to Purchase Ratios (Category and Subcategory)**: Ratios of wishlist actions to purchases for both category and subcategory.
- **Click Wishlist to Purchase Ratios (Category and Subcategory)**: Ratios of clicks on wishlist to purchases for both category and subcategory.
- **Product View to Purchase Ratios (Category and Subcategory)**: Ratios of product views to purchases for both category and subcategory.

### Output

The prediction endpoint returns the predicted probability of the user making a purchase, expressed as a percentage.

## 5. Dockerfile and Containerization

The Dockerfile provided in the project repository allows for containerizing the Customer Propensity Model application using a multi-stage build strategy. This strategy helps reduce the size of the final Docker image by separating the build dependencies from the runtime environment.

### Dockerfile Explanation

The Dockerfile consists of two stages:

1. **Builder Stage**: In this stage, a Python 3.8 slim-buster image is used to install the project dependencies specified in the `requirements.txt` file. This stage sets the working directory to `/install` and copies only the `requirements.txt` file to leverage Docker's caching mechanism. It then installs the dependencies into the `/install` directory using `pip`. This stage is responsible for creating a temporary image used for building the dependencies.

2. **Final Stage**: The final Docker image is created based on another Python 3.8 slim-buster image. This stage sets the working directory to `/app` and copies the installed dependencies from the builder stage into the `/usr/local` directory. It then copies the rest of the application files into the `/app` directory. After copying, any unnecessary files are cleaned up to reduce the image size. Finally, the command to run the Flask application is specified using the `CMD` directive, which starts the Flask server on `0.0.0.0:5000`.

### Building the Docker Image

To build the Docker image for the Customer Propensity Model application, navigate to the project directory containing the Dockerfile and execute the following command:

```bash
docker build -t customer-propensity-model .
```

Once the Docker image is built, you can run a Docker container using the following command:
```bash
docker run -d -p 5000:5000 customer-propensity-model
```
This command will start a Docker container based on the customer-propensity-model image, exposing port 5000 on the host machine. You can then access the Customer Propensity Model application by visiting http://localhost:5000 in your web browser


## 6. CI/CD Pipelines

The project utilizes GitHub Actions for Continuous Integration (CI) and Continuous Delivery (CD) pipelines to automate the testing, building, and deployment processes.
![1_jrdZWe4JRU5KDbWfnRxenA](https://github.com/prxdyu/customer_propensity_modelling/assets/105141574/dd8b33fe-5755-498c-83d7-24db2c807857)


### Continuous Integration (CI)

The CI pipeline ensures the correctness and reliability of the Customer Propensity Model application by running automated tests using pytest. These tests validate the functionality of key endpoints in the Flask application. The test.py file is responsible for running the tests to ensure the proper running of flask application

#### Test Workflow

- **Workflow Name**: Containerizing the Image and deploying it to EC2
- **Trigger**: Automatically triggered upon pushing changes to the `main` branch.
- **Jobs**:
  - **Job 1**: Runs tests with pytest.
  - **Job 2**: Deploys the Docker image to Amazon EC2 instance.

### Continuous Delivery (CD)

The CD pipeline automates the deployment of the Docker image containing the Flask application to an Amazon EC2 instance.

#### Workflow Steps

1. **Checkout**: Checks out the code from the repository.
2. **Install Python 3**: Sets up the Python environment for testing.
3. **Install Dependencies**: Installs project dependencies listed in `requirements_dev.txt`.
4. **Run tests with pytest**: Executes automated tests using pytest.
5. **Print AWS Secrets**: Prints AWS access keys for authentication.
6. **Configure AWS Credentials**: Configures AWS credentials for accessing services.
7. **Login to Amazon ECR**: Logs in to Amazon Elastic Container Registry (ECR) for container image storage.
8. **Build, tag, push image to Amazon ECR**: Builds the Docker image, tags it, and pushes it to Amazon ECR.
9. **Deploy docker image from ECR to EC2 instance**: Deploys the Docker image from ECR to an EC2 instance, running the Flask application.

These CI/CD pipelines ensure the application is thoroughly tested and efficiently deployed to the production environment, enhancing development productivity and maintaining application quality.



