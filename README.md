[![Stories in Ready](https://badge.waffle.io/HewlettPackard/oneview-redfish-toolkit.png?label=ready&title=Ready)](http://waffle.io/HewlettPackard/oneview-redfish-toolkit) [![Build Status](https://travis-ci.org/HewlettPackard/oneview-redfish-toolkit.svg?branch=master)](https://travis-ci.org/HewlettPackard/oneview-redfish-toolkit)

# HPE OneView Redfish Toolkit

This toolkit provides a REST service to answer DMTF's Redfish compliant requests by querying HPE OneView.

HPE OneView is a fresh approach to converged infrastructure management, inspired by the way you expect to work, with a single integrated view of your IT infrastructure.

DMTF's Redfish is an open industry standard specification and schema that specifies a RESTful interface and utilizes JSON and OData to help customers integrate solutions within their existing tool chains.

## Installation

### Requirements

HPE OneView Redfish Toolkit service relies on Python 3.5 or newer (as long as python3 executable is available) to run and [pip3](https://pip.pypa.io/en/stable/installing/) for dependencies management. A full list of dependencies is available at [requirements.txt](requirements.txt) file. For pyOpenSSL module please make sure to have OpenSSL lib installed in your system.

> There should be not problem in using Python 3.4 if your system does not have Python 3.5 available, but we do not guarantee complete compatibility as the test environment is set up on version 3.5.

In order to run tests and documentation generation `tox` is also needed. General instructions on how to install are available [here](https://tox.readthedocs.io/en/latest/install.html).

### From source

We recommend to run inside a virtual environment. You can create one running:

```bash
$ virtualenv env_name_you_choose -p python3.5 # to create a Python3.5 environment, for example
$ source env_name_you_choose/bin/activate # load the environment
```

Once the environment is loaded, download and uncompress the latest version from [releases page](https://github.com/HewlettPackard/oneview-redfish-toolkit/releases), or clone current development version running:

```bash
$ git clone https://github.com/HewlettPackard/oneview-redfish-toolkit.git
```

Then, proceed with:

```bash
$ cd oneview-redfish-toolkit # enter the service folder
# edit redfish.conf
$ pip install -r requirements.txt # to install all requirements into the virtual environment
$ ./run.sh    # to launch the service
```

## SDK Documentation

The latest version of the SDK documentation can be found in the [SDK Documentation section](https://hewlettpackard.github.io/oneview-redfish-toolkit/index.html).

> Note: This documentation has been manually updated following the steps found [here](https://github.com/HewlettPackard/python-hpOneView/blob/master/deploy.sh).

## Logging

Logging configuration can be found in `logging.conf` file. The provided configuration enables INFO level at both console and file output (which will generate a `redfish.log` file).

## Configuration

In order to start up oneview-redfish-toolkit service, there is some mandatory configuration at `redfish.conf` file to provide as explained below:

* `redfish` section

  * **schema_dir**: path to where DTMF's Redfish JSON schemas are stored
  
  * **indent_json**: whether JSON objects on answers are indented or not

  * **xml_prettify**: whether XML objects on answers are indented or not

  * **redfish_host**: the IP address where redfish service will listen to. Using `host = 0.0.0.0` means it will listen to all IP addresses.

  * **redfish_port**: the TCP port where redfish service will listen to

  * **authentication_mode**: can be one of: `conf` or `session`. In `conf` mode authentication credentials from the conf file will be used for all requests. In `session` mode the user must authenticate himself using his own username and password doing a post request to `/redfish/v1/SessionService/Sessions`, passing the parameters UserName and Password in the body. The user will get an `x-auth-token` from this operation and all subsequent operations should send this token as a `x-auth-token` header. The `/redfish` and `/redfish/v1` endpoints can be accessed without authentication. If mode is set to `session` any other request to endpoints apart from those mentioned above are going to be rejected if they don't send a valid `x-auth-token` header.
  

* `oneview` section

  * **ip**: HPE OneView's IP or FQDN address
  
  * **api_version**: HPE OneView's version. Defaults to 300.

* `credentials` section

  * **username**: HPE OneView's username
  
  * **password**: HPE OneView's password

* `event_service` section

  * **DeliveryRetryAttempts**: The value of this property shall be the number of retrys attempted for any given event to the subscription destination before the subscription is terminated.
  
  * **DeliveryRetryIntervalSeconds**: The value of this property shall be the interval in seconds between the retry attempts for any given event to the subscription destination.

* `ssl` section

  * **SSLType**: How to configure SSL. One of: disabled (no SSL), adhoc (SSL is enabled with self-signed keys generated by the server every time you start the server), self-signed (SSL is enabled with a self-signed cert generated in the certs directory if no files named self-signed.crt and self-signed.key exists in that directory. This will create the certificates on the first run and every time you delete the files and restart the server. The directory **certs must** exist in the system root directory) certs (SSL is enabled with keys provided by user in the fields below). The default value used is adhoc.
  
  * **SSLCertFile**: The user SSL cert file.

  * **SSLKeyFile**: The user SSL key file. Should not have a password.

* `ssl-cert-defaults` section: Defines the values used in the self-signed generated certificate

  * **countryName**: The name of the country. **Required!**
  
  * **stateOrProvinceName**: The name of the state or province. **Required!**

  * **localityName**: Name of the locality (city for example). **Required!**

  * **organizationName**: Name of the organization (company name for example). **Required!**
  
  * **organizationalUnitName**: Name of the organizational unit (department for example). **Required!**

  * **commonName**: FQDN of the server or it's IP address. If not provided will detect de default route IP and use it. **Optional.**
 
  * **emailAddress**: Email address to contact the responsible for this server/certificate. This is an optional information. Will not be added to certificate if not informed. **Optional.**

* `schemas` section

  * **ServiceRoot**: DTMF's Redfish JSON schema for the `Service Root` resource
  
  * **ChassisCollection**: DTMF's Redfish JSON schema for `Chassis` collections
  
  * **Chassis**: DTMF's Redfish JSON schema for `Chassis` resources
  
  * **ComputerSystemCollection**: DTMF's Redfish JSON schema for `Computer Systems` collections
  
  * **ComputerSystem**: DTMF's Redfish JSON schema for `Computer Systems` resources
  
  * **ManagerCollection**: DTMF's Redfish JSON schema for `Managers` collections
  
  * **Manager**: DTMF's Redfish JSON schema for `Manager` resources
  
  * **EventService**: DTMF's Redfish JSON schema for the `Event Service` resource
  
  * **EventDestination**: DTMF's Redfish JSON schema for `Event Destination` resources
  
  * **Event**: DTMF's Redfish JSON schema for `Event` objects

Note: HPE OneView' credentials are stored in clear-text. Make sure only authorized users can access this file.

## Event Service notes:

Currently, Event Service works only when authentication_mode is set to conf. As it connects directly to HPE OneView SCMB, the toolkit will request OneView to generate SCMB certs and/or download the certs to the correct location. The certs file are: **oneview\_ca**: OneView's CA cert file located at: `certs/oneview_ca.pem`. **scmb\_cert**: OneView's SCMB Client cert file located at: `certs/oneview_scmb.pem`. **scmb\_key**: OneView's SCMB Client key file located at: `certs/oneview_scmb.key`


## Contributing

You know the drill. Fork it, branch it, change it, commit it, and pull-request it. We are passionate about improving this project, and are glad to accept help to make it better. However, keep the following in mind:

We reserve the right to reject changes that we feel do not fit the scope of this project. For feature additions, please open an issue to discuss your ideas before doing the work.

## Feature Requests

If you have a need not being met by the current implementation, please let us know (via a new issue). This feedback is crucial for us to deliver a useful product. Do not assume that we have already thought of everything, because we assure you that is not the case.

## Testing

We have already packaged everything you need to do to verify if the code is passing the tests. The tox script wraps the unit tests execution against Python 3, flake8 validation, and the test coverage report generation.

Run the following command:

```
$ tox
```

## License

This project is licensed under the Apache License 2.0.
