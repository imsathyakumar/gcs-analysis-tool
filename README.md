#GCS Analysis Tool
GCS Analytics tool is created for providing more information on a given Google cloud Storage's Bucket information in a tabular format.

##Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the Google cloud SDKs to run the tool
```bash
pip install -r requirements.txt
```

<br/>

###Point to note
For querying Google Storage for Objects, Service accounts are the best to be used for this purpose to avoid "quota exceeded" or "API not enabled" error. 
For more information about service accounts, see https://cloud.google.com/docs/authentication/.
<br/>

##Usage
```bash
$ python gcs_analysis_tool.py -h                                                              
usage: gcs_analysis_tool.py [-h] -p PROJECTID [-x PREFIX] [-l] [-f FILTER]

optional arguments:
  -h, --help            show this help message and exit
  -p PROJECTID, --projectid PROJECTID
                        Example : -p gpc-dev
  -x PREFIX, --prefix PREFIX
                        Bucket name prefix. Example : -x transaction [for
                        filtering transaction-data bucket]
  -l, --listbuckets     List the bucket names alone
  -f FILTER, --filter FILTER
                        Example [-f location:US]. Available options:
                        bucket_size, time_created, file_count, time_modified,
                        bucket_price, location, storage_class,
                        lifecyle_enabled
```
<br/>

###Examples
To list only the bucketnames in the Project:
```bash
$ python gcs_analysis_tool.py -p test-dev -l                                    
Bucket Name
----------------------------------------------------------
test-separation-test
test-dev
test-dev-artifacts
test-dev-bootstrap
test-dev-data
test-dev-nat-gateway
test-dev-rawdata
test-dev-sre
```

The option `-x` which is used as bucket prefix, can be combined with `-l`
```bash
$ python gcs_analysis_tool.py -p test-dev -l -x test-separation                                    
Bucket Name
----------------------------------------------------------
test-separation-test
```

To list all buckets and its complete metadata:
```bash
$ python gcs_analysis_tool.py -p test-dev -x dataproc
╒════════════════════════════════════════════════════════════╤══════════════════════════╤═══════════════════╤══════════════╤══════════════════════════╤══════════╤══════════════╤═════════════════╤═════════════════════╕
│ Bucket Name                                                │ Creation time            │   Number of files │ Total size   │ Last Modified            │ Cost     │ Location     │ Storage class   │ Lifecycle Enabled   │
╞════════════════════════════════════════════════════════════╪══════════════════════════╪═══════════════════╪══════════════╪══════════════════════════╪══════════╪══════════════╪═════════════════╪═════════════════════╡
│ dataproc-test1-sgdajfjasdjadfjfgjhjhsdfjhsdgs-us-east1     │ 2019-02-09T19:35:27.612Z │                 8 │ 1.3MB        │ 2019-02-09T19:35:27.612Z │ $0       │ US-EAST1     │ STANDARD        │ False               │
├────────────────────────────────────────────────────────────┼──────────────────────────┼───────────────────┼──────────────┼──────────────────────────┼──────────┼──────────────┼─────────────────┼─────────────────────┤
│ dataproc-test2-q345sfd245asfzsdfg5346sd46ysd2-us-central1  │ 2019-02-09T19:24:26.899Z │                 8 │ 1.3MB        │ 2019-02-09T19:24:26.899Z │ $0       │ US-CENTRAL1  │ STANDARD        │ False               │
├────────────────────────────────────────────────────────────┼──────────────────────────┼───────────────────┼──────────────┼──────────────────────────┼──────────┼──────────────┼─────────────────┼─────────────────────┤
│ dataproc-test3-2q45awrq35te234srf236sdfdre42e-us           │ 2019-01-12T09:00:09.088Z │              2201 │ 199.8MB      │ 2019-01-12T09:00:09.088Z │ $0.00017 │ US           │ STANDARD        │ False               │
├────────────────────────────────────────────────────────────┼──────────────────────────┼───────────────────┼──────────────┼──────────────────────────┼──────────┼──────────────┼─────────────────┼─────────────────────┤
│ dataproc-test4-q345dfgsdq34tadfsg345qwasfdfg3-europe-west4 │ 2019-02-09T21:36:02.386Z │                 1 │ 2.9KB        │ 2019-02-09T21:36:02.386Z │ $0       │ EUROPE-WEST4 │ STANDARD        │ False               │
╘════════════════════════════════════════════════════════════╧══════════════════════════╧═══════════════════╧══════════════╧══════════════════════════╧══════════╧══════════════╧═════════════════╧═════════════════════╛

```

To filter the results, `-f` is used with specific headers.<br/>
It supports below filters:

* bucket_size
* time_created
* file_count
* time_modified
* bucket_price
* location
* storage_class
* lifecyle_enabled

```bash
$ python gcs_analysis_tool.py -p test-dev -x dataproc -f 'location:us'
╒════════════════════════════════════════════════════════════╤══════════════════════════╤═══════════════════╤══════════════╤══════════════════════════╤══════════╤══════════════╤═════════════════╤═════════════════════╕
│ Bucket Name                                                │ Creation time            │   Number of files │ Total size   │ Last Modified            │ Cost     │ Location     │ Storage class   │ Lifecycle Enabled   │
╞════════════════════════════════════════════════════════════╪══════════════════════════╪═══════════════════╪══════════════╪══════════════════════════╪══════════╪══════════════╪═════════════════╪═════════════════════╡
│ dataproc-test1-sgdajfjasdjadfjfgjhjhsdfjhsdgs-us-east1     │ 2019-02-09T19:35:27.612Z │                 8 │ 1.3MB        │ 2019-02-09T19:35:27.612Z │ $0       │ US-EAST1     │ STANDARD        │ False               │
├────────────────────────────────────────────────────────────┼──────────────────────────┼───────────────────┼──────────────┼──────────────────────────┼──────────┼──────────────┼─────────────────┼─────────────────────┤
│ dataproc-test2-q345sfd245asfzsdfg5346sd46ysd2-us-central1  │ 2019-02-09T19:24:26.899Z │                 8 │ 1.3MB        │ 2019-02-09T19:24:26.899Z │ $0       │ US-CENTRAL1  │ STANDARD        │ False               │
├────────────────────────────────────────────────────────────┼──────────────────────────┼───────────────────┼──────────────┼──────────────────────────┼──────────┼──────────────┼─────────────────┼─────────────────────┤
│ dataproc-test3-2q45awrq35te234srf236sdfdre42e-us           │ 2019-01-12T09:00:09.088Z │              2201 │ 199.8MB      │ 2019-01-12T09:00:09.088Z │ $0.00017 │ US           │ STANDARD        │ False               │    │
╘════════════════════════════════════════════════════════════╧══════════════════════════╧═══════════════════╧══════════════╧══════════════════════════╧══════════╧══════════════╧═════════════════╧═════════════════════╛

```

###Improvements TODO
1. Get tool to sort any given field
2. Get tool to filter based on Total size [greater/lesser than]
3. Get tool to find the percentage of space used by each individual Buckets

###Author
Sathyanarayanan Kumar - [ImSathyaKumar](https://github.com/imsathyakumar)