"""GCS Analysis tool to provide the below information on all Buckets for any given Google project
    1. Bucket name
    2. Creation date (of the bucket)
    3. Number of files
    4. Total size of files
    5. Last modified date (most recent file of a bucket)
    6. how much does it cost
   Also capable of providing additional Bucket information and filters

Point to note:
    Google client library automatically look for the credentials in the environment.
    For an already authenticated user, App credentials will be in ~/.config/gcloud/application_default_credentials.json
    For a new user, pls run 'gcloud auth login' to get authenticated.
    For Service account, pls export the env variable GOOGLE_APPLICATION_CREDENTIALS=[PATH]/[KEY_FILE]"""

import argparse
import warnings

# We need Google's storage module to run the tool
try:
    from google.cloud import storage
except ImportError:
    raise ImportError("storage is not installed, please run "
                      "'pip install --upgrade google-cloud-storage' to install.")

# We need tabulate module to print nicely formatted table
try:
    from tabulate import tabulate
except ImportError:
    raise ImportError(
        "tabulate not installed, please run 'pip install  tabulate' to install.")

# Covered below in README
warnings.filterwarnings(
    "ignore", "Your application has authenticated using end user credentials")


parser = argparse.ArgumentParser()
parser.add_argument("-p", "--projectid", help="Example : -p gpc-dev", required=True)
parser.add_argument("-x", "--prefix", help="Bucket name prefix. Example : -x transaction "
                                           "[for filtering transaction-data bucket]")
parser.add_argument("-l", "--listbuckets", help="List the bucket names alone", action='store_true')
parser.add_argument("-f", "--filter", help="Example [-f location:US]. Available options: bucket_size, "
                                           "time_created, file_count, time_modified, bucket_price, "
                                           "location, storage_class, lifecyle_enabled ")
args = parser.parse_args()

# Creating storage client
try:
    storage_client = storage.Client(project=args.projectid)
except Exception as e:
    raise e


def list_buckets(prefix=None):
    """List all buckets in the given project"""
    try:
        buckets_list = list(storage_client.list_buckets(prefix=prefix))
        return buckets_list
    except Exception as e:
        raise e


def get_bucket_info(bucketname):
    """Retrieves metadata for the given bucket"""
    try:
        bucketobj = storage_client.get_bucket(bucketname)
        blobs = bucketobj.list_blobs()
    except Exception as e:
        raise e
    bucketsize = 0
    for blob in blobs:
        bucketsize += blob.size
    filecount = blobs.num_results
    return bucketsize, filecount


def size_conversion(size_bytes):
    """Converts given byte size to human readable"""
    for unit in ['', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB']:
        if abs(size_bytes) < 1024.0:
            return "%3.1f%s" % (size_bytes, unit)
        size_bytes /= 1024.0
    return "%.1f%s" % (size_bytes, 'YB')


def get_pricing_info(bucketsize, location):
    """Finds the approx price calculation of the bucket on the given day
    In GCP, only Multi Regional storage is charged"""
    if location is 'MULTI_REGIONAL' or location == 'US':
        charge_per_gb_per_month = 0.026
        return "$%.5f" % (bucketsize*charge_per_gb_per_month/1073741824/30)  # considering 30 days per month & based on bytes
    else:
        return "$0"


def print_table(bucketdict):
    """Prints the entire bucket metadata"""
    table = []
    headers = ("Bucket Name", "Creation time", "Number of files", "Total size", "Last Modified", "Cost", "Location",
               "Storage class", "Lifecycle Enabled")
    for eachbucket, bucketvalues in bucketdict.iteritems():
        table.append((eachbucket, bucketvalues['time_created'], bucketvalues['file_count'], bucketvalues['bucket_size']
                      , bucketvalues['time_modified'], bucketvalues['bucket_price'], bucketvalues['location']
                      , bucketvalues['storage_class'], bucketvalues['lifecyle_enabled']))
    print tabulate(table, headers, "fancy_grid").encode('utf-8')


try:
    buckets = list_buckets(args.prefix)
except Exception as e:
    raise e

if args.listbuckets:  # lists only the bucket names
    bucketnameonly = []
    for bucket_iter in buckets:
        bucketnameonly.append(bucket_iter._properties['name'])
    print tabulate([[i] for i in bucketnameonly], ["Bucket Name"], "simple").encode('utf-8')

else:  # captures detailed bucket info
    bucket = {}
    for bucket_iter in buckets:
        bucket_name = bucket_iter._properties['name']
        (bucket_size, file_count) = get_bucket_info(bucket_name)
        location = bucket_iter._properties['location']
        bucket[bucket_name] = dict(time_created=bucket_iter._properties['timeCreated'], file_count=file_count,
                                   bucket_size=size_conversion(bucket_size), time_modified=bucket_iter._properties['updated'],
                                   location=location,
                                   storage_class=bucket_iter._properties['storageClass'],
                                   bucket_price=get_pricing_info(bucket_size, location),
                                   lifecyle_enabled=bucket_iter.versioning_enabled)

    if args.filter:
        filter_key = args.filter.split(':')[0]
        filter_value = args.filter.split(':')[1]
        filtered_bucket = {k: v for k, v in bucket.iteritems() if filter_value.lower() in str(v[filter_key]).lower()}
        print_table(filtered_bucket)
    else:
        print_table(bucket)
