# Building a Test-Cricket Statistics Pipeline with Google Cloud Services
In the world of data engineering, the journey from data retrieval to insightful visualization is an adventure filled with challenges and rewards. In this guide, I'll walk through the intricate steps of constructing a comprehensive cricket statistics pipeline using GCP services. From retrieving data via the Cricbuzz API to crafting a dynamic Looker Studio dashboard, each phase contributes to the seamless flow of data for analysis and visualization.

### Architecture
![Architecture](https://github.com/sakshamsaxena06984/gcp-data-harvest-pipelines/blob/main/pipelines-architecture/cricbuzz-pipeline-architecture.png)

### Data Retrieval with Python and Cricbuzz API
The foundation of Test-Cricket-Players-Ranking pipeline begins with Python’s prowess in interfacing with APIs. We’ll delve into the methods of fetching cricket statistics from the Cricbuzz API, harnessing the power of Python to gather the required data efficiently.

### Storing Data in Google Cloud Storage (GCS)
Once the data is obtained, our next step involves preserving it securely in the cloud. We’ll explore how to store this data in a CSV format within Google Cloud Storage (GCS), ensuring accessibility and scalability for future processing.

### Dataflow Job for BigQuery
The core of our pipeline lies in the Dataflow job. Triggered by the Cloud Function, this job orchestrates the transfer of data from the CSV file in GCS to BigQuery. We’ll meticulously configure the job settings to ensure optimal performance and accurate data ingestion into BigQuery.


### Looker Dashboard Creation
Finally, I can explore the potential of BigQuery as a data source for Looker Studio. Configuring Looker to connect with BigQuery, we’ll create a visually compelling dashboard. This dashboard will serve as the visualization hub, enabling insightful analysis based on the data loaded from our cricket statistics pipeline.
![Looker](https://github.com/sakshamsaxena06984/gcp-data-harvest-pipelines/blob/main/visualization-reports/cricbuzz-test-ply-rnks-looker.png)

### Orchestration 
To orchestrate a scalable data pipeline using Cloud Composer, Created an Airflow DAG with two tasks: one for executing a Python script for preprocessing, and another for launching a Dataflow job to handle distributed data transformation.
