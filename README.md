# Update Prices of a GSheet File with Bull Market ONs Information.

**The ON price data has a delay of 20 minutes**

### How to setup the Updater

#### 1. Install the required libraries with pipenv
pipenv is a library that is used to create a virtualenv with the required packages. Documentation can be found in https://pipenv.pypa.io/en/latest/

Once pipenv is installed is time to install the required packages.

1.1 Open a terminal in your working directory and activate a virtualenv with the following command

    pipenv shell

1.2 Install the packages with the command

    pipenv install

#### 2. Upload the .xlsx file to Google Sheets
Upload the .xlsx file that is located in the folder *gsheet example* to your own Google Sheet

#### 3. Create a Google Service Account
3.1 Go to https://console.cloud.google.com/ and create a project or you can use the default one
3.2 In the navigator menu go to *IAM and admin* and choose *Service Accounts*
3.3 Click in *+ CREATE A SERVICE ACCOUNT*
3.4 Choose a *Service account name* and a *Service account ID* that you wish and click *DONE*
3.5 Click in the 3 dots at the right of the service account that you have just created and choose the option *Manage keys*
3.6 Click in *ADD KEY*, *Create new key*. Choose *json* and *CREATE*. This is going to download a json file with the Service Account credentials. This file has to be copied into the *settings* folder
3.7 Rename the json credential file with the following name: gsheet-on-updater-credentials.json

#### 4. Share the Google Sheet with your Service Account
4.1 From the previous website copy the Service Account Email. For example: *updater-service-account@my-project.iam.gserviceaccount.com*
4.2 In your Google Sheet click SHARE and add your Service Account Email as Editor

#### 2. Run the script
Every time that you restart the terminal you have to re-activate the virtual environment with the command

    pipenv shell

Then you have to run the file **main.py** in the console:

    python main.py