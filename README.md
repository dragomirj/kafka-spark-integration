# Apache Kafka and Apache Spark integration
# Overview
Streaming and analyzing data streams from smart systems using Apache Kafka 
and Apache Spark tools.

This project showcases an [**Event-Driven Architecture (EDA)**](https://www.confluent.io/learn/event-driven-architecture/) 
by integrating Apache Kafka with Apache Spark. Apache Kafka is utilized as a 
real-time data pipeline due to its low latency and high throughput 
(more than a million messages per second). Apache Spark is deployed 
to run basic computations (average) on data that has been grouped 
based on a 15-second time window and the device name.

# How scripts communicate
![How scripts communicate](img/communication.png?raw=true "How scripts communicate")

# Quick Start
You must have [**Apache Kafka**](https://kafka.apache.org/) and 
[**Apache Spark**](https://spark.apache.org/) up and running before running this project. 
The project was built with Apache Kafka version ***2.13-3.4.1*** and Apache Spark 
version ***3.5.0***. The next step is to install Python, preferably ***3.11***, 
as well as all of the dependencies listed in the `requirements.txt` file.

## Installation
*For more information about Python's virtual environment and its importance, please refer to this* [***Wiki***](https://docs.python.org/3.11/library/venv.html).

**Windows:**
```
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install -r requirements.txt
```

**Linux:**
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

# Step-by-Step
## Deploy Apache Spark script
Dependencies make it challenging to deploy Apache Spark scripts with Python. 
The code below will execute `spark.py` locally with as many worker threads as 
your machine's logical cores (*master parameter*) and the required dependencies.
To learn more about how to deploy an Apache Spark application, you can check the 
[**official documentation**](https://spark.apache.org/docs/latest/submitting-applications.html).

```
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 \
    --class org.apache.spark.examples.SparkPi \
    --master local[*] \
    ./spark.py \
    1000
```

## Start `app.py` client application
The client application is a simple Flask web application with only one route, the home route, 
and a SocketIO broadcast event function. [**SocketIO**](https://socket.io/) was designed to 
facilitate real-time applications, which this project intends to demonstrate. It is important to 
mention that the home route uses *SocketIO*'s async mode, which implies that there should be 
a listener on the main page. 

```
python app.py
```

## Start the `device.py` scripts
This script reads the carbon monoxide level from the MQ-2 sensor and broadcasts it to the 
system using MQTT. To run this script, connect the Arduino, which has the `mq2_co_reader.ino` 
running, to a Raspberry Pi via USB. The script can be run without these devices; however, 
the data will be generated randomly with a uniform distribution.

Execute both scripts in order to see the problem with data streaming: It is impossible 
to determine the order in which events arrive. 

```
python device1.py
```

```
python device2.py
```

## Start the `bridge.py` script
The following script subscribes to the provided MQTT topic and retrieves data, 
which is then transmitted to Apache Kafka.

```
python bridge.py
```

Below is an example of a JSON string that is sent to Apache Kafka.

```json
{
    "timestamp": "2024-10-07 13:02:54.927410",
    "device_name": "device2",
    "data": 863.85
}
```

## Start the `emitter.py` script
The following script will retrieve the data analysis from Apache Kafka. 
The data is eventually broadcasted to all connected clients via SocketIO.

```
python emitter.py
```

Below is an example of a JSON string that is broadcasted via SocketIO.

```json
{
    "device_name": "device1",
    "window_start": "15:29:15",
    "window_end": "15:29:30",
    "data": 606.891
}
```

# Additional Documentation
There is extra documentation available for the [**Arduino code**](/arduino/README.md) 
that reads data from the MQ-2 sensor.

# Testing
The project was tested using Python's unit testing framework. The tests can be found in 
the [**tests**](tests) directory. The output of the `bridge.py` script must match that 
of the `device1.py` and `device2.py` scripts; thus, no unit tests are necessary.

# License
Distributed under the GNU License. See [*LICENSE*](LICENSE) for more information.