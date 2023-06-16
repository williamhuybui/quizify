text_1 = """
Asia is the largest of the world’s continents, covering approximately 30 percent of the Earth’s land area. It is also the world’s most populous continent, with roughly 60 percent of the total population.

Asia makes up the eastern portion of the Eurasian supercontinent; Europe occupies the western portion. The border between the two continents is debated. However, most geographers define Asia’s western border as an indirect line that follows the Ural Mountains, the Caucasus Mountains, and the Caspian and Black Seas. Asia is bordered by the Arctic, Pacific, and Indian Oceans.

Asia’s physical geography, environment and resources, and human geography can be considered separately.

Asia can be divided into five major physical regions: mountain systems; plateaus; plains, steppes, and deserts; freshwater environments; and saltwater environments.
"""

example_1 = [
    {
        "question": "What percentage of the Earth’s land area does Asia cover?",
        "options": ["20 percent", "30 percent", "40 percent", "50 percent"],
        "answer": "30 percent",
    },
    {
        "question": "What percentage of the world’s population does Asia have?",
        "options": ["30 percent", "40 percent", "50 percent", "60 percent"],
        "answer": "60 percent",
    },
    {
        "question": "Which continent occupies the western portion of the Eurasian supercontinent?",
        "options": ["Europe", "North America", "South America", "Africa"],
        "answer": "Europe",
    },
    {
        "question": "What is the debated border between Asia and Europe?",
        "options": [
            "The Ural Mountains",
            "The Himalayan Mountains",
            "The Rocky Mountains",
            "The Appalachian Mountains",
        ],
        "answer": "The Ural Mountains",
    },
    {
        "question": "Which oceans border Asia?",
        "options": [
            "Atlantic and Indian",
            "Pacific and Atlantic",
            "Pacific and Indian",
            "Arctic and Antarctic",
        ],
        "answer": "Arctic, Pacific, and Indian",
    },
    {
        "question": "How many major physical regions can Asia be divided into?",
        "options": ["3", "4", "5", "6"],
        "answer": "5",
    },
    {
        "question": "Which physical region of Asia includes freshwater environments?",
        "options": [
            "Mountain systems",
            "Plateaus",
            "Plains, steppes, and deserts",
            "Freshwater environments",
        ],
        "answer": "Freshwater environments",
    },
    {
        "question": "Which physical region of Asia includes saltwater environments?",
        "options": [
            "Mountain systems",
            "Plateaus",
            "Saltwater environments",
            "Plains, steppes, and deserts",
        ],
        "answer": "Saltwater environments",
    },
    {
        "question": "What is the western border of Asia?",
        "options": [
            "Ural Mountains, Caucasus Mountains, and Caspian and Black Seas",
            "Himalayan Mountains",
            "Rocky Mountains",
            "Appalachian Mountains",
        ],
        "answer": "Ural Mountains, Caucasus Mountains, and Caspian and Black Seas",
    },
    {
        "question": "What is the eastern portion of the Eurasian supercontinent?",
        "options": ["Europe", "Asia", "North America", "South America"],
        "answer": "Asia",
    },
]

text_2 = """
Modern Cloud Data Platform

Databricks is an American enterprise software company founded by the creators of Apache Spark.[2] Databricks develops a web-based platform for working with Spark, that provides automated cluster management and IPython-style notebooks. The company develops Delta Lake, an open-source project to bring reliability to data lakes for machine learning and other data science use cases.[3]

History [ edit ]

Databricks grew out of the AMPLab project at University of California, Berkeley that was involved in making Apache Spark, an open-source distributed computing framework built atop Scala. The company was founded by Ali Ghodsi, Andy Konwinski, Arsalan Tavakoli-Shiraji, Ion Stoica, Matei Zaharia,[4] Patrick Wendell, and Reynold Xin.

In November 2017, the company was announced as a first-party service on Microsoft Azure via the integration Azure Databricks.[5]

In June 2020, Databricks acquired Redash, an open-source tool designed to help data scientists and analysts visualize and build interactive dashboards of their data.[6]

In February 2021 together with Google Cloud, Databricks provided integration with the Google Kubernetes Engine and Google's BigQuery platform.[7] Fortune ranked Databricks as one of the best large "Workplaces for Millennials" in 2021.[8] At the time, the company said more than 5,000 organizations used its products.[9]

In August 2021, Databricks finished their eighth round of funding by raising $1.6 billion and valuing the company at $38 billion.[10]

In October 2021, Databricks made its second acquisition of German no-code company 8080 Labs. 8080 Labs makes bamboolib, a data exploration tool that does not require coding to use.[11]

In response to the popularity of OpenAI's ChatGPT, in March 2023, the company introduced an open-source language model, named Dolly after Dolly the sheep, that developers could use to create their own chatbots. Their model uses fewer parameters to produce similar results as ChatGPT, but Databricks had not released formal benchmark tests to show whether its bot actually matched the performance of ChatGPT.[12][13][14]

Databricks acquired data security startup Okera in May 2023 to extend its data governance capabilities.[15]

Funding [ edit ]

In September 2013, Databricks announced it raised $13.9 million from Andreessen Horowitz and said it aimed to offer an alternative to Google's MapReduce system.[16][17] Microsoft was a noted investor of Databricks in 2019, participating in the company's Series E at an unspecified amount.[18][19] The company has raised $1.9 billion in funding, including a $1 billion Series G led by Franklin Templeton at a $28 billion post-money valuation in February 2021. Other investors include Amazon Web Services, CapitalG (a growth equity firm under Alphabet Inc.) and Salesforce Ventures.[9]

Products [ edit ]

Databricks develops and sells a cloud data platform using the marketing term "lakehouse", a portmanteau based on the terms "data warehouse" and "data lake".[27] Databricks' lakehouse is based on the open source Apache Spark framework that allows analytical queries against semi-structured data without a traditional database schema.[28] In October 2022, Lakehouse received FedRAMP authorized status for use with the U.S. federal government and contractors.[29]

Databricks' Delta Engine launched in June 2020 as a new query engine that layers on top of Delta Lake to boost query performance.[30] It is compatible with Apache Spark and MLflow, which are also open source projects from Databricks.[31]

In November 2020, Databricks introduced Databricks SQL (previously known as SQL Analytics) for running business intelligence and analytics reporting on top of data lakes. Analysts can query data sets directly with standard SQL or use product connectors to integrate directly with business intelligence tools like Tableau, Qlik, SigmaComputing, Looker, and ThoughtSpot.[32]

Databricks offers a platform for other workloads, including machine learning, data storage and processing, streaming analytics, and business intelligence.[33]

The company has also created Delta Lake, MLflow and Koalas, open source projects that span data engineering, data science and machine learning.[34] In addition to building the Databricks platform, the company has co-organized massive open online courses about Spark[35] and a conference for the Spark community called the Data + AI Summit,[36] formerly known as Spark Summit.

Operations [ edit ]

Databricks is headquartered in San Francisco.[37] It also has operations in Canada, the United Kingdom, Netherlands, Singapore, Australia, Germany, France, Japan, China, South Korea, India, and Brazil.[38]
"""
example_2 = [
    {
        "question": "What was Databricks originally a part of?",
        "options": [
            "AMPLab project at University of California, Berkeley",
            "Computer Science Department at Stanford University",
            "Artificial Intelligence lab at Massachusetts Institute of Technology",
            "None of the above",
        ],
        "answer": "AMPLab project at University of California, Berkeley",
    },
    {
        "question": 'In response to the popularity of which tool did Databricks introduce its open-source language model "Dolly"?',
        "options": [
            "Google Assistant",
            "Amazon Alexa",
            "IBM Watson",
            "OpenAI's ChatGPT",
        ],
        "answer": "OpenAI's ChatGPT",
    },
    {
        "question": "What is the name of the German no-code company acquired by Databricks in October 2021?",
        "options": ["Bamboolib", "8080 Labs", "Redash", "Okera"],
        "answer": "8080 Labs",
    },
    {
        "question": "What service was announced as a first-party service on Microsoft Azure in November 2017?",
        "options": ["Databricks", "Apache Spark", "Delta Lake", "None of the above"],
        "answer": "Databricks",
    },
    {
        "question": "What is the total funding Databricks has raised?",
        "options": ["$1.6 billion", "$1.9 billion", "$38 billion", "None of the above"],
        "answer": "$1.9 billion",
    },
    {
        "question": "What marketing term does Databricks use for its cloud data platform?",
        "options": ["Data pool", "Data ocean", "Data stream", "Lakehouse"],
        "answer": "Lakehouse",
    },
]
