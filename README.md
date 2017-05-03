# Promotions API

[![Build Status](https://travis-ci.org/NYU-DEVOPS-INDIA/PROMOTIONS.svg?branch=master)](https://travis-ci.org/NYU-DEVOPS-INDIA/PROMOTIONS)
[![codecov](https://codecov.io/gh/NYU-DEVOPS-INDIA/PROMOTIONS/branch/master/graph/badge.svg)](https://codecov.io/gh/NYU-DEVOPS-INDIA/PROMOTIONS)

Team India

To run this API locally : 

```{r, engine='bash', count_lines}
$ git clone https://github.com/NYU-DEVOPS-INDIA/PROMOTIONS.git
$ cd PROMOTIONS
$ vagrant up
$ vagrant ssh
$ cd /vagrant
$ python server_promotion.py
```

When running locally, the API can be accessed from the URL : http://192.168.33.10:5000

Bluemix Docker URL : http://nyu-devops-promotion-docker.mybluemix.net/

Cloud Foundry URL: https://nyudevops-promotions-service.mybluemix.net/

Swagger URL: https://nyu-devops-promotion-docker.mybluemix.net/apidocs/index.html?url=/v1/spec#/
