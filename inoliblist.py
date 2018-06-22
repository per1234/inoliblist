# for command line arguments
import argparse
# for writing the CSV file
import csv
# for automatically generating unique column indexes
import enum
# for URL request errors
import http.client
# for parsing Library Manager index
import json
# for debug output
import logging
# for parsing page count from response header
import re
# for handling rate limiting timeouts
import time
# for URL request errors
import urllib.error
# for normalizing URLs
import urllib.parse
# for URL requests
import urllib.request

# configuration parameters:

# (s) interval between printing GitHub API rate limit reset wait messages
rate_limit_reset_wait_notification_interval = 300
# (s) delay after rate limit reset time to make sure it has actually reset before the next API request
rate_limit_reset_wait_additional_delay = 180

# call check_rate_limiting() after an exception that stars with this string
# urllib.error.HTTPError: HTTP Error 503: Service Unavailable
check_rate_limiting_after_exception = "HTTPError: HTTP Error 503"
# retry urlopen after exceptions that start with the following strings
# urllib.error.HTTPError: HTTP Error 403: Forbidden
urlopen_retry_exceptions = ["HTTPError: HTTP Error 403",
                            # urllib.error.HTTPError: HTTP Error 502: Bad Gateway
                            "HTTPError: HTTP Error 502",
                            check_rate_limiting_after_exception,
                            # http.client.RemoteDisconnected: Remote end closed connection without response
                            # https://circleci.com/gh/per1234/inoliblist/4
                            "RemoteDisconnected",
                            # ConnectionResetError: [Errno 104] Connection reset by peer
                            # https://circleci.com/gh/per1234/inoliblist/25
                            "ConnectionResetError"
                            ]

# delay before retry after failed urlopen (seconds)
urlopen_retry_delay = 60
# maximum times to retry opening the URL before giving up
maximum_urlopen_retries = 5

# maximum number of results per API request (max allowed by GitHub is 100)
results_per_page = 100

# (s) delay before retrying search
search_retry_delay = 60
# maximum times to retry the search when it returns incomplete or no results
maximum_search_retries = 10

# when verification is enabled, repositories that match the following regular expressions will be skipped
repository_name_blacklist = ["arduino",
                             "sketchbook"
                             ]

# regular expressions for administrative files whitelist to use to determine whether subfolders should be searched
# during library verification
administrative_file_whitelist = ["^\..*",  # starts with .
                                 "^[^\.]*$",  # doesn't contain .
                                 "^.*\.adoc$",
                                 "^.*\.md$",
                                 "^.*\.rst$",
                                 "^.*\.txt$",
                                 "^platformio.ini$"
                                 ]

# library header file extensions recognized by the Arduino IDE
header_file_extensions = [".h", ".hh", ".hpp"]

# regular expressions for common library examples folder names
examples_folder_names = ["^examples$",
                         "^example$"
                         ]

# regular expressions fo subfolders to skip when searching the repository for a library
library_subfolder_blacklist = ["^\..*",
                               "bin",
                               "data",
                               "doc",
                               "docs",
                               "example",
                               "examples",
                               "extras",
                               "graphics",
                               "hardware",
                               "img",
                               "images",
                               "lib",
                               "scripts",
                               "test",
                               "tests",
                               "tools"
                               ]

output_filename = "inoliblist.csv"
output_file_delimiter = '\t'
output_file_quotechar = None

# DEBUG: automatically generated output and all higher log level output
# INFO: manually specified output and all higher log level output
logging_level = logging.INFO
# allow all log output to be disabled
logging.addLevelName(1000, "OFF")
# default to no logger
logging.basicConfig(level="OFF")
logger = logging.getLogger(__name__)


# ensure all columns are given unique indexes
@enum.unique
# automatically define column indexes
class ColumnEnum(enum.IntEnum):
    repository_url = 0
    repository_owner = enum.auto()
    repository_name = enum.auto()
    repository_default_branch = enum.auto()
    library_path = enum.auto()
    archived = enum.auto()
    is_fork = enum.auto()
    fork_of = enum.auto()
    last_push_date = enum.auto()
    fork_count = enum.auto()
    star_count = enum.auto()
    contributor_count = enum.auto()
    tip_status = enum.auto()
    repository_license = enum.auto()
    repository_language = enum.auto()
    repository_description = enum.auto()
    github_topics = enum.auto()
    in_library_manager_index = enum.auto()
    # in_platformio_library_registry = enum.auto()
    library_manager_name = enum.auto()
    library_manager_version = enum.auto()
    library_manager_author = enum.auto()
    library_manager_maintainer = enum.auto()
    library_manager_sentence = enum.auto()
    library_manager_paragraph = enum.auto()
    library_manager_category = enum.auto()
    library_manager_url = enum.auto()
    library_manager_architectures = enum.auto()
    platformio_name = enum.auto()
    platformio_description = enum.auto()
    platformio_keywords = enum.auto()
    platformio_authors = enum.auto()
    platformio_repository = enum.auto()
    platformio_version = enum.auto()
    platformio_license = enum.auto()
    platformio_download_url = enum.auto()
    platformio_homepage = enum.auto()
    platformio_frameworks = enum.auto()
    platformio_platforms = enum.auto()
    count = enum.auto()


# convert the enums to ints
class Column:
    repository_url = int(ColumnEnum.repository_url)
    repository_owner = int(ColumnEnum.repository_owner)
    repository_name = int(ColumnEnum.repository_name)
    repository_default_branch = int(ColumnEnum.repository_default_branch)
    library_path = int(ColumnEnum.library_path)
    archived = int(ColumnEnum.archived)
    is_fork = int(ColumnEnum.is_fork)
    fork_of = int(ColumnEnum.fork_of)
    last_push_date = int(ColumnEnum.last_push_date)
    fork_count = int(ColumnEnum.fork_count)
    star_count = int(ColumnEnum.star_count)
    contributor_count = int(ColumnEnum.contributor_count)
    tip_status = int(ColumnEnum.tip_status)
    repository_license = int(ColumnEnum.repository_license)
    repository_language = int(ColumnEnum.repository_language)
    repository_description = int(ColumnEnum.repository_description)
    github_topics = int(ColumnEnum.github_topics)
    in_library_manager_index = int(ColumnEnum.in_library_manager_index)
    # in_platformio_library_registry=int(ColumnEnum.in_platformio_library_registry)
    library_manager_name = int(ColumnEnum.library_manager_name)
    library_manager_version = int(ColumnEnum.library_manager_version)
    library_manager_author = int(ColumnEnum.library_manager_author)
    library_manager_maintainer = int(ColumnEnum.library_manager_maintainer)
    library_manager_sentence = int(ColumnEnum.library_manager_sentence)
    library_manager_paragraph = int(ColumnEnum.library_manager_paragraph)
    library_manager_category = int(ColumnEnum.library_manager_category)
    library_manager_url = int(ColumnEnum.library_manager_url)
    library_manager_architectures = int(ColumnEnum.library_manager_architectures)
    platformio_name = int(ColumnEnum.platformio_name)
    platformio_description = int(ColumnEnum.platformio_description)
    platformio_keywords = int(ColumnEnum.platformio_keywords)
    platformio_authors = int(ColumnEnum.platformio_authors)
    platformio_repository = int(ColumnEnum.platformio_repository)
    platformio_version = int(ColumnEnum.platformio_version)
    platformio_license = int(ColumnEnum.platformio_license)
    platformio_download_url = int(ColumnEnum.platformio_download_url)
    platformio_homepage = int(ColumnEnum.platformio_homepage)
    platformio_frameworks = int(ColumnEnum.platformio_frameworks)
    platformio_platforms = int(ColumnEnum.platformio_platforms)
    count = int(ColumnEnum.count)


# globals
table = [[""] * Column.count]
github_token = None
enable_verbosity = False
# setting these to 0 will force a check to determine the actual values on the first request
last_api_requests_remaining_value = {"search": 0, "core": 0}


def main():
    """The primary function."""
    set_github_token(github_token_input=argument.github_token)
    set_verbosity(enable_verbosity_input=argument.enable_verbosity)
    initialize_table()
    populate_table()
    create_output_file()


def set_verbosity(enable_verbosity_input):
    """Turn debug output on or off.

    Keyword arguments:
    enable_verbosity_input -- this will generally be controlled via the script's --verbose command line argument
                              (True, False)
    """
    global enable_verbosity
    if enable_verbosity_input:
        enable_verbosity = True
        logger.setLevel(level=logging_level)
    else:
        enable_verbosity = False
        logger.setLevel(level="OFF")


def set_github_token(github_token_input):
    """Configure the script to use a GitHub personal API access token.
    This will result in a more generous API request allowance and thus the list will be generated faster.
    See: https://developer.github.com/v3/#rate-limiting

    Keyword arguments:
    github_token_input -- a GitHub personal API access token
                          see: https://blog.github.com/2013-05-16-personal-api-tokens/
    """
    if github_token_input is None:
        logger.warning("set_github_token() was passed an empty token string.")
    global github_token
    github_token = github_token_input


def get_github_token():
    """Returns the GitHub Personal Access Token. Used for checking the value in the unit test."""
    return github_token


def populate_table():
    """Create a list of Arduino library repositories and their useful metadata. This list is stored in the global list
     variable 'table'.
     """
    logger.info("Processing the Library Manager index.")
    json_data = dict(get_json_from_url(url="http://downloads.arduino.cc/libraries/library_index.json")["json_data"])
    process_library_manager_index(json_data=json_data)

    logger.info("Processing GitHub's arduino-library topic.")
    # GitHub API search gives a max of 1000 results per search query so to avoid losing results I split the searches by
    #  repo creation date
    search_repositories(search_query="topic:arduino-library",
                        created_argument_list=["<=2018-05-29",
                                               ">=2018-05-30"],
                        fork_argument="true",
                        verify=False)

    logger.info("Processing GitHub's arduino topic.")
    search_repositories(search_query="topic:arduino",
                        created_argument_list=["<=2016-03-23",
                                               "2016-03-24..2017-01-07",
                                               "2017-01-08..2017-03-22",
                                               "2017-03-23..2017-06-15",
                                               "2017-06-16..2017-09-18",
                                               "2017-09-19..2017-12-19",
                                               "2017-12-20..2018-03-07",
                                               "2018-03-08..2018-06-05",
                                               ">=2018-06-06"],
                        fork_argument="true",
                        verify=True)

    logger.info("Processing GitHub search for arduino library.")
    search_repositories(search_query="arduino+library+topics:0+language:cpp+language:c+language:arduino",
                        created_argument_list=["<=2012-12-25",
                                               "2012-12-26..2013-12-27",
                                               "2013-12-28..2014-10-05",
                                               "2014-10-06..2015-04-28",
                                               "2015-04-29..2015-11-25",
                                               "2015-11-26..2016-05-18",
                                               "2016-05-19..2016-11-20",
                                               "2016-11-21..2017-04-14",
                                               "2017-04-15..2017-09-18",
                                               "2017-09-19..2018-01-31",
                                               "2018-02-01..2018-06-12",
                                               ">=2018-06-13"],
                        fork_argument="false",
                        verify=True)


def initialize_table():
    """Fill in the first row of the table with the heading text."""
    # clear the table (necessary to avoid conflict between unit tests)
    global table
    table = [[""] * Column.count]

    # fill the column headings row
    table[0][Column.repository_url] = "Repository URL \x1b \x1b"
    table[0][Column.repository_owner] = "Owner \x1b \x1b"
    table[0][Column.repository_name] = "Repo Name \x1b \x1b"
    table[0][Column.repository_default_branch] = "Default Branch \x1b \x1b"
    table[0][Column.library_path] = "Library Path \x1b \x1b"
    table[0][Column.archived] = "Archived \x1b \x1b"
    table[0][Column.is_fork] = "Fork \x1b \x1b"
    table[0][Column.fork_of] = "Fork Of \x1b \x1b"
    table[0][Column.last_push_date] = "Last Push \x1b \x1b"
    table[0][Column.fork_count] = "#Forks \x1b \x1b"
    table[0][Column.star_count] = "#Stars \x1b \x1b"
    table[0][Column.contributor_count] = "#Contributors \x1b \x1b"
    table[0][Column.tip_status] = "Status \x1b \x1b"
    table[0][Column.repository_license] = "License \x1b \x1b"
    table[0][Column.repository_language] = "Language \x1b \x1b"
    table[0][Column.repository_description] = "Repo Description \x1b \x1b"
    table[0][Column.github_topics] = "GitHub Topics \x1b \x1b"
    table[0][Column.in_library_manager_index] = "In Library Manager \x1b \x1b"
    # table[0][Column.in_platformio_library_registry] = "In PlatformIO \x1b \x1b"
    table[0][Column.library_manager_name] = "LM name \x1b \x1b"
    table[0][Column.library_manager_version] = "LM version \x1b \x1b"
    table[0][Column.library_manager_author] = "LM author \x1b \x1b"
    table[0][Column.library_manager_maintainer] = "LM maintainer \x1b \x1b"
    table[0][Column.library_manager_sentence] = "LM sentence \x1b \x1b"
    table[0][Column.library_manager_paragraph] = "LM paragraph \x1b \x1b"
    table[0][Column.library_manager_category] = "LM category \x1b \x1b"
    table[0][Column.library_manager_url] = "LM url \x1b \x1b"
    table[0][Column.library_manager_architectures] = "LM architectures \x1b \x1b"
    table[0][Column.platformio_name] = "PIO name \x1b \x1b"
    table[0][Column.platformio_description] = "PIO description \x1b \x1b"
    table[0][Column.platformio_keywords] = "PIO keywords \x1b \x1b"
    table[0][Column.platformio_authors] = "PIO authors \x1b \x1b"
    table[0][Column.platformio_repository] = "PIO repository \x1b \x1b"
    table[0][Column.platformio_version] = "PIO version \x1b \x1b"
    table[0][Column.platformio_license] = "PIO license \x1b \x1b"
    table[0][Column.platformio_download_url] = "PIO downloadUrl \x1b \x1b"
    table[0][Column.platformio_homepage] = "PIO homepage \x1b \x1b"
    table[0][Column.platformio_frameworks] = "PIO frameworks \x1b \x1b"
    table[0][Column.platformio_platforms] = "PIO platforms \x1b \x1b"


def get_table():
    """Return the table global variable. Used by the unit tests to check the value."""
    return table


def get_github_api_response(request, request_parameters="", page_number=1):
    """Do a GitHub API request. Return a dictionary containing:
    json_data -- JSON object containing the response
    additional_pages -- indicates whether more pages of results remain (True, False)
    page_count -- total number of pages of results

    Keyword arguments:
    request -- the section of the URL following https://api.github.com/
    request_parameters -- GitHub API request parameters (see: https://developer.github.com/v3/#parameters)
                          (default value: "")
    page_number -- Some responses will be paginated. This argument specifies which page should be returned.
                   (default value: 1)
    """
    if request.startswith("search"):
        api_type = "search"
    else:
        api_type = "core"
    check_rate_limiting(api_type=api_type)

    return get_json_from_url(url="https://api.github.com/" +
                                 request + "?" +
                                 request_parameters +
                                 "&page=" + str(page_number) +
                                 "&per_page=" + str(results_per_page)
                             )


def check_rate_limiting(api_type):
    """Check whether the GitHub API request limit has been reached.
    If so, delay until the request allotment is reset before returning.

    Keyword arguments:
    api_type -- GitHub has two API types, each with their own limits and allotments.
                "search" applies only to api.github.com/search.
                "core" applies to all other parts of the API.
    """
    global last_api_requests_remaining_value
    if last_api_requests_remaining_value[api_type] == 0:
        # the stored requests remaining value might be outdated (because the limit reset since the last API request) so
        #  I need to actually do an request to the Rate Limit API to get the real number
        # the rate_limit API does not use up the API request allotment so I can use get_json_from_url()
        json_data = dict(get_json_from_url(url="https://api.github.com/rate_limit")["json_data"])

        last_api_requests_remaining_value["core"] = json_data["resources"]["core"]["remaining"]
        last_api_requests_remaining_value["search"] = json_data["resources"]["search"]["remaining"]
        rate_limiting_reset_time = json_data["resources"][api_type]["reset"] + rate_limit_reset_wait_additional_delay

        logger.info(api_type + " API request allotment: " + str(json_data["resources"][api_type]["limit"]))
        logger.info("Remaining " + api_type + " API requests: " + str(last_api_requests_remaining_value[api_type]))
        logger.info(api_type + " API rate limiting reset time: " + str(rate_limiting_reset_time))

        if last_api_requests_remaining_value[api_type] == 0:
            # API request allowance is used up
            if github_token is None:
                print("Pass the script a GitHub personal API access token via the --ghtoken command line argument " +
                      "for a more generous allowance")
                print("https://blog.github.com/2013-05-16-personal-api-tokens/")
            notification_timestamp = 0
            while time.time() < rate_limiting_reset_time:
                # print a periodic message while waiting for the API timeout to indicate the script is still alive
                if (time.time() - notification_timestamp) > rate_limit_reset_wait_notification_interval:
                    print(
                        "GitHub " + api_type + " API request limit reached. Time before limit reset: " +
                        str(int((rate_limiting_reset_time - time.time()) / 60)) + " minutes"
                    )
                    notification_timestamp = time.time()
            # leave the last_api_requests_remaining_value[api_type] set to 0
            # this will cause the actual value to be pulled from the API on the next check_rate_limiting() call
            check_rate_limiting(api_type=api_type)
        else:
            logger.warning("Mismatch between stored requests remaining value (0) and actual value")


def get_json_from_url(url):
    """Load the specified URL and return a dictionary:
    json_data -- JSON object containing the response
    additional_pages -- indicates whether more pages of results remain (True, False)
    page_count -- total number of pages of results

    Keyword arguments:
    url -- the URL to load
    """
    url = normalize_url(url=url)

    logger.info("Opening URL: " + url)

    retry_count = 0
    while retry_count <= maximum_urlopen_retries:
        retry_count += 1
        if url.startswith("https://api.github.com"):
            # the topics data is currently in preview mode so a custom media type must be provided in the Accept header
            # to get it (https://developer.github.com/v3/repos/#list-all-topics-for-a-repository)
            headers = {"Accept": "application/vnd.github.mercy-preview+json"}
            if github_token is not None:
                # GitHub provides more generous API request allotments when authenticated so a Personal Access Token is
                # passed via the header
                headers["Authorization"] = "token " + str(github_token)

            request = urllib.request.Request(url=url, headers=headers)
        else:
            request = urllib.request.Request(url=url)
        try:
            with urllib.request.urlopen(request) as url_data:
                try:
                    json_data = json.loads(url_data.read().decode("utf-8", "ignore"))
                except json.decoder.JSONDecodeError as exception:
                    # output some information on the exception
                    logger.warning(str(exception.__class__.__name__) + ": " + str(exception))
                    # pass on the exception to the caller
                    raise exception

                if not json_data:
                    # there was no HTTP error but an empty page was returned (e.g. contributors request when the repo
                    # has 0 contributors)
                    # an empty page is not returned after a search with no results but the items array is empty so
                    # search_repositories() handles that correctly
                    page_count = 0
                    additional_pages = False
                else:
                    # get the number of pages of results from the response header
                    # this is currently only used for GitHub API requests but it sounds like the Link header is a common
                    # convention so it may be useful for other applications as well
                    page_count = 1
                    additional_pages = False

                    if url_data.info()["Link"] is not None:
                        if url_data.info()["Link"].find(">; rel=\"next\"") != -1:
                            additional_pages = True
                        for link in url_data.info()["Link"].split(','):
                            if link[-13:] == ">; rel=\"last\"":
                                link = re.split("[?&>]", link)
                                for parameter in link:
                                    if parameter[:5] == "page=":
                                        page_count = parameter.split('=')[1]
                                        break
                                break

                # get the number of GitHub API requests from the response header
                if url.startswith("https://api.github.com") and url_data.info()["X-RateLimit-Remaining"] is not None:
                    global last_api_requests_remaining_value
                    if url.startswith("https://api.github.com/search"):
                        last_api_requests_remaining_value["search"] = int(url_data.info()["X-RateLimit-Remaining"])
                    else:
                        last_api_requests_remaining_value["core"] = int(url_data.info()["X-RateLimit-Remaining"])

                return {"json_data": json_data, "additional_pages": additional_pages, "page_count": page_count}
        except Exception as exception:
            if not determine_urlopen_retry(exception=exception):
                raise exception

    # maximum retries reached without successfully opening URL
    raise TimeoutError("Maximum number of URL load retries exceeded")


def determine_urlopen_retry(exception):
    """Determine whether the exception warrants another attempt at opening the URL.
    If so, delay then return True. Otherwise, return False.

    Keyword arguments:
    exception -- the exception
    """
    exception_string = str(exception.__class__.__name__) + ": " + str(exception)
    logger.info(exception_string)
    for urlopen_retry_exception in urlopen_retry_exceptions:
        if str(exception_string).startswith(urlopen_retry_exception):
            # these errors may only be temporary, retry
            print("Temporarily unable to open URL (" + str(exception) + "), retrying")
            if exception_string.startswith(check_rate_limiting_after_exception):
                # ideally this would only be done if the URL opened was api.github.com and use the correct API type but
                # it should do no real harm as is
                check_rate_limiting(api_type="core")
                check_rate_limiting(api_type="search")
            time.sleep(urlopen_retry_delay)
            return True

    # other errors are probably permanent so give up
    if str(exception_string).startswith("urllib.error.HTTPError: HTTP Error 401"):
        print(exception)
        print("HTTP Error 401 may be caused by providing an incorrect GitHub personal access token.")
    return False


def normalize_url(url):
    """Replace problematic characters in the URL and return it.

    Keyword arguments:
    url -- the URL to process
    """
    url_parts = urllib.parse.urlparse(url)
    # url_parts is a tuple but I need to change values so it's necessary to convert it to list
    url_parts = list(url_parts)
    for url_part in enumerate(url_parts):
        # do percent-encoding on the URL (e.g. change space to %20) and replace any occurrences of multiple slashes with
        # a single slash
        url_parts[url_part[0]] = urllib.parse.quote(url_part[1].replace("///", "/").replace("//", "/"), safe="&=?/+")
    return urllib.parse.urlunparse(url_parts)


def process_library_manager_index(json_data):
    """Parse the Arduino Library Manager index's JSON and add all libraries to the list.
    This function is split out from populate_table() for unit tests.
    """
    # step through all the libraries in the Library Manager index
    last_repository_url = ""
    for library_data in json_data["libraries"]:
        # get the repository URL as listed in the Library Manager index (which may be different from the GitHub URL if
        # the repository has been renamed, due to GitHub automatically redirecting the URL
        repository_url = library_data["repository"]
        # don't add duplicate rows for libraries with multiple tags. Although I check for duplicates in populate_row(),
        # this prevents unnecessary GitHub API calls.
        if repository_url != last_repository_url:
            # for now I'm only listing GitHub repos
            if repository_url.split('/')[2] == "github.com":
                repository_name = repository_url.split('/')[3] + '/' + repository_url.split('/')[4][:-4]
                populate_row(repository_object=get_github_api_response(request="repos/" + repository_name)["json_data"],
                             in_library_manager=True,
                             verify=False)
            last_repository_url = repository_url


def search_repositories(search_query, created_argument_list, fork_argument, verify):
    """Use the GitHub API to search for repositories and pass the results to populate_row()
    (see: https://developer.github.com/v3/search/#search-repositories)

    Keyword arguments:
    search_query -- the search query
    created_argument_list -- repository creation date range to filter results by
                             (see: https://help.github.com/articles/understanding-the-search-syntax/#query-for-dates)
    fork_argument -- fork filter. Valid values are "true", "false", "only".
                     (see: https://help.github.com/articles/searching-in-forks/)
    verify -- whether to verify that results contain an Arduino library (allowed values: True, False)
    """
    for created_argument in created_argument_list:
        search_results_count = 0
        # handle pagination
        page_number = 1
        additional_pages = True
        while additional_pages:
            # sort by forks because this is the least frequently changing sort property (can't sort by creation date)
            # changing properties (esp. updated) will cause the search results order to change between pages,
            # leading to duplicates and skips

            do_github_api_request_return = ()
            json_data = ()

            incomplete_results = True
            search_retry_count = 0
            while incomplete_results and search_retry_count < maximum_search_retries:
                search_retry_count += 1
                do_github_api_request_return = get_github_api_response(request="search/repositories",
                                                                       request_parameters="q=" + search_query +
                                                                                          "+created:" +
                                                                                          created_argument +
                                                                                          "+fork:" + fork_argument +
                                                                                          "&sort=forks&order=desc",
                                                                       page_number=page_number)
                json_data = dict(do_github_api_request_return["json_data"])

                if json_data["incomplete_results"]:
                    # I have seen this happen, then on the next try it was fine
                    print("Search results are incomplete due to a timeout. Retrying. " +
                          "See: https://developer.github.com/v3/search/#timeouts-and-incomplete-results")
                    time.sleep(search_retry_delay)
                elif json_data["total_count"] == 0:
                    # I'm don't know if this would occur for any reason that would be resolved by retrying
                    print("Search returned 0 results. Retrying.")
                    # don't delay since this causes a super long delay during the unit test and it's not clear this
                    # retry even serves any purpose
                else:
                    incomplete_results = False

            additional_pages = do_github_api_request_return["additional_pages"]
            page_number += 1
            for repository_object in json_data["items"]:
                search_results_count += 1

                if verify:
                    repository_name_is_blacklisted = False
                    for blacklisted_repository_name_regex in repository_name_blacklist:
                        blacklisted_repository_name_regex = re.compile(blacklisted_repository_name_regex,
                                                                       flags=re.IGNORECASE
                                                                       )
                        if blacklisted_repository_name_regex.fullmatch(repository_object["name"]):
                            repository_name_is_blacklisted = True
                            break
                    if repository_name_is_blacklisted:
                        # skip this repository
                        continue

                populate_row(repository_object=repository_object, in_library_manager=False, verify=verify)

            if not additional_pages and search_results_count < json_data["total_count"]:
                # GitHub's search API provides data for a maximum of 1000 search results
                # https://developer.github.com/v3/search/#about-the-search-api
                # to work around this I have broken the searches into created date segments
                # but these will need to be updated over time as more repositories are added that match the searches
                logger.warning(
                    "Maximum search results count reached for search segment: " + created_argument +
                    " in query: " + search_query
                )

        logger.info("Found " + str(search_results_count) +
                    " search results for search segment: " + created_argument +
                    " in query: " + search_query
                    )


def populate_row(repository_object, in_library_manager, verify):
    """Populate a row of the list with data for the repository.

    Keyword arguments:
    repository_object -- object containing the GitHub API data for a repository
    in_library_manager -- value to store in the "In Library Manager" column (True, False)
    verify -- whether to verify the repository contains an Arduino library (allowed values: True, False)
    """
    global table

    logger.info("Attempting to populate row for: " + repository_object["html_url"])

    # check if it's already on the list
    for readRow in table:
        if readRow[Column.repository_url] == repository_object["html_url"]:
            # it's already on the list
            logger.info("Skipping duplicate: " + repository_object["html_url"])
            return

    # initialize the row list
    row_list = [""] * Column.count

    library_folder = find_library_folder(repository_object=repository_object,
                                         row_list=row_list,
                                         verify=verify)
    if library_folder is None:
        if verify:
            # verification is required and a library was not found so skip the repo
            logger.info("Skipping (library verification failed)")
            return
        library_folder = ""

    row_list[Column.library_path] = library_folder

    row_list[Column.repository_url] = str(repository_object["html_url"])
    row_list[Column.repository_owner] = str(repository_object["owner"]["login"])
    row_list[Column.repository_name] = str(repository_object["name"])
    row_list[Column.repository_default_branch] = str(repository_object["default_branch"])
    row_list[Column.archived] = str(repository_object["archived"])
    row_list[Column.is_fork] = str(repository_object["fork"])

    if repository_object["fork"]:
        try:
            row_list[Column.fork_of] = str(repository_object["parent"]["full_name"])
        except KeyError:
            # the repository data in the search results is missing some items:
            # "parent", "source", "network_count", "subscribers_count"
            # I need the "parent" object to get the fork parent so I need to to a whole other API request to get the
            # full repository object to pass to populate_row
            # this is not necessary for the repos from the Library Manager index since their repository_object already
            # comes from the repos API
            do_github_api_request_return = get_github_api_response(request="repos/" +
                                                                           repository_object["full_name"]
                                                                   )
            # replace search API version of repository_object with the full repos API version
            repository_object = dict(do_github_api_request_return["json_data"])
            row_list[Column.fork_of] = str(repository_object["parent"]["full_name"])

    row_list[Column.last_push_date] = str(repository_object["pushed_at"])
    row_list[Column.fork_count] = str(repository_object["forks_count"])
    row_list[Column.star_count] = str(repository_object["stargazers_count"])
    row_list[Column.contributor_count] = get_contributor_count(repository_object=repository_object)

    do_github_api_request_return = get_github_api_response(request="repos/" +
                                                                   repository_object["full_name"] +
                                                                   "/commits/" +
                                                                   repository_object["default_branch"] +
                                                                   "/status"
                                                           )
    status_data = dict(do_github_api_request_return["json_data"])
    if str(status_data["state"]) != "pending":
        row_list[Column.tip_status] = str(status_data["state"])
    else:
        # the term "pending" used by GitHub for commits with no status would be confusing
        row_list[Column.tip_status] = ""

    row_list[Column.repository_license] = get_repository_license(repository_object=repository_object)
    row_list[Column.repository_language] = str(repository_object["language"])

    if repository_object["description"] is not None:
        row_list[Column.repository_description] = str(repository_object["description"])

    # comma-separated list of topics
    row_list[Column.github_topics] = ', '.join(repository_object["topics"])
    row_list[Column.in_library_manager_index] = str(in_library_manager)
    # Not currently implemented. Neither the PlatformIO API or platformio lib provide the URL of the library so I'm not
    # sure this will even be possible.
    # row_list[Column.in_platformio_library_registry] =

    # replace tabs with spaces so they don't mess up the TSV
    # strip leading and trailing whitespace
    for index, cell in enumerate(row_list):
        row_list[index] = cell.replace('\t', "    ").strip()

    # provide an indication of script progress
    if enable_verbosity:
        for cell in row_list:
            logger.info(cell)
    else:
        print(row_list[Column.repository_url])

    # add the new row to the table
    table.append(row_list)


def find_library_folder(repository_object, row_list, verify):
    """Scan a repository to try to find the location of the library.
    Return the folder name where the library was found or None if not found.

    Keyword arguments:
    repository_object -- the repository's JSON
    row_list -- the list being populated by populate_row(). Information from any metadata files found during the search
                will be added to this list.
    verify -- if verification is enabled then it is required that the library be found in the root of the repository
              and measures will be taken to avoid mistaking a sketch for a library. If verification is not enabled then
              subfolders of the library will also be checked. (True, False)
    """
    # start with a blind attempt to open and parse a metadata file in the repository root to avoid unnecessary GitHub
    # API requests
    library_folder = None
    if parse_library_dot_properties(metadata_folder="/",
                                    repository_object=repository_object,
                                    row_list=row_list
                                    ):
        # don't return after finding library.properties because library.json should also be parsed if present
        library_folder = "/"

    if parse_library_dot_json(metadata_folder="/",
                              repository_object=repository_object,
                              row_list=row_list
                              ):
        library_folder = "/"

    if library_folder is not None:
        # metadata file was found in the repo root folder
        return library_folder
    # metadata file was not found in the repo root folder

    if not verify:
        # attempt a blind attempt to open /{repo name}.h to reduce API requests
        url = normalize_url(url="https://raw.githubusercontent.com/" +
                                repository_object["full_name"] + "/" +
                                repository_object["default_branch"] + "/" +
                                repository_object["name"] + ".h"
                            )
        logger.info("Opening URL: " + url)
        try:
            with urllib.request.urlopen(url):
                pass
            # header file found
            return "/"
        except (urllib.error.HTTPError, http.client.RemoteDisconnected) as exception:
            # don't bother retrying on possibly recoverable exceptions
            logger.info(str(exception.__class__.__name__) + ": " + str(exception))
            pass

    # get a listing of the root folder contents
    page_number = 1
    additional_pages = True
    root_folder_listing = []
    while additional_pages:
        try:
            do_github_api_request_return = get_github_api_response(request="repos/" +
                                                                           repository_object["full_name"] +
                                                                           "/contents",
                                                                   page_number=page_number)
        except urllib.error.HTTPError:
            # a 404 error is returned for API requests for empty repositories
            logger.info("Skipping empty repository")
            return None
        except (json.decoder.JSONDecodeError, TimeoutError):
            logger.warning("Could not load contents API for the root folder of repo.")
            if verify:
                logger.info("Skipping because unable to verify repository")
                return None
            else:
                logger.info("Adding repository to list with unknown library folder.")
                return None

        page_number += 1
        additional_pages = do_github_api_request_return["additional_pages"]
        root_folder_listing += list(do_github_api_request_return["json_data"])

    library_found = find_library(folder_listing=root_folder_listing, verify=verify)
    if library_found:
        return "/"
    if verify:
        if library_found is None:
            # check subfolders
            pass
        elif not library_found:
            return None

    # library not found in repo root but so search one subfolder down
    for root_folder_item in root_folder_listing:
        if root_folder_item["type"] == "dir":
            # skip blacklisted subfolder names
            folder_is_blacklisted = False
            for blacklisted_subfolder_regex in library_subfolder_blacklist:
                blacklisted_subfolder_regex = re.compile(blacklisted_subfolder_regex, flags=re.IGNORECASE)
                if blacklisted_subfolder_regex.fullmatch(root_folder_item["name"]):
                    # the folder name matched the blacklist regular expression
                    folder_is_blacklisted = True
                    break
            if folder_is_blacklisted:
                continue

            # get a listing of the subfolder contents
            page_number = 1
            additional_pages = True
            subfolder_listing = []
            while additional_pages:
                try:
                    do_github_api_request_return = get_github_api_response(request="repos/" +
                                                                                   repository_object["full_name"] +
                                                                                   "/contents/" +
                                                                                   root_folder_item["name"],
                                                                           page_number=page_number)
                except(json.decoder.JSONDecodeError, urllib.error.HTTPError, TimeoutError):
                    # I already know the repo is not empty but I don't know what would happen for an empty
                    # folder since Git doesn't currently support them:
                    # https://git.wiki.kernel.org/index.php/GitFaq#Can_I_add_empty_directories.3F
                    # but I'll assume it would be a 404, which will cause get_github_api_response to return None
                    logger.warning(
                        "Something went wrong during API request for contents of " + root_folder_item[
                            "name"] + " folder. Moving on to the next folder...")
                    break

                page_number += 1
                additional_pages = do_github_api_request_return["additional_pages"]
                subfolder_listing += list(do_github_api_request_return["json_data"])

            if find_library(folder_listing=subfolder_listing, verify=verify):
                # library was found in this folder
                # parse metadata files if present
                parse_library_dot_properties(metadata_folder=root_folder_item["name"],
                                             repository_object=repository_object,
                                             row_list=row_list)
                parse_library_dot_json(metadata_folder=root_folder_item["name"],
                                       repository_object=repository_object,
                                       row_list=row_list)
                return root_folder_item["name"]

    # library folder not found
    return None


def find_library(folder_listing, verify):
    """Determine whether the folder contains a library.

    Keyword arguments:
    folder_listing -- list of the folder contents
    verify -- if verification is enabled then it is required that the library be found in the root of the repository
              and measures will be taken to avoid mistaking a sketch for a library. If verification is not enabled then
              subfolders of the library will also be checked. (True, False)

    Return values:
    True -- library found
    None -- Library not found but verification didn't fail
    False -- Library not found
    """

    metadata_file_found = False
    keywords_dot_txt_found = False
    header_file_found = False
    sketch_file_found = False
    examples_folder_found = False
    only_administrative_files_found = True

    for folder_item in folder_listing:
        if folder_item["type"] == "file":
            if folder_item["name"] == "library.properties":
                metadata_file_found = True
            elif folder_item["name"] == "library.json":
                metadata_file_found = True
            elif folder_item["name"] == "keywords.txt":
                keywords_dot_txt_found = True
            else:
                for header_file_extension in header_file_extensions:
                    if folder_item["name"].endswith(str(header_file_extension)):
                        header_file_found = True
        # these checks are only required for verification
        if verify:
            # check for sketch files in repo root
            if folder_item["type"] == "file":
                if (
                        folder_item["name"].endswith(".ino") or
                        folder_item["name"].endswith(".pde")
                ):
                    sketch_file_found = True

                is_administrative_file = False
                for administrative_file_regex in administrative_file_whitelist:
                    administrative_file_regex = re.compile(administrative_file_regex, flags=re.IGNORECASE)
                    if administrative_file_regex.fullmatch(folder_item["name"]):
                        is_administrative_file = True
                        break
                if not is_administrative_file:
                    only_administrative_files_found = False
            # check for examples folder in repo root
            elif folder_item["type"] == "dir":
                for examples_folder_name_regex in examples_folder_names:
                    examples_folder_name_regex = re.compile(examples_folder_name_regex, flags=re.IGNORECASE)
                    if examples_folder_name_regex.fullmatch(folder_item["name"]):
                        examples_folder_found = True
                        break

    if verify:
        # to pass verification, the repo must meet one of the following:
        # - has metadata file in root
        # - has header file and no sketch file in root
        # - has header file and either examples (or some variant) folder or keywords.txt in root
        # - has only administrative files in the root and a subfolder meets one of the above
        if metadata_file_found:
            # metadata is sufficient whether or not verification is required
            return True
        elif header_file_found and not sketch_file_found:
            # verification passed
            return True
        elif header_file_found and sketch_file_found and (
                examples_folder_found or keywords_dot_txt_found):
            # verification passed
            return True
        elif only_administrative_files_found:
            # only administrative files were found in the root so check the subfolders too
            return None
        else:
            # verification failed
            return False
    else:
        if metadata_file_found:
            return True
        if header_file_found:
            # if verification is off then just finding a header file is enough
            return True
        else:
            # library not found
            return False


def parse_library_dot_properties(metadata_folder, repository_object, row_list):
    """Attempt to open the file library.properties from the specified folder of the repository.
    If successful, parse the contents, fill cells of the row with the data, return True.
    If unsuccessful, return False.

    Keyword arguments:
    metadata_folder -- the folder of the repository containing library.properties
    repository_object -- the JSON object containing the repository data
    row_list -- the list to populate with data from the parsed library.properties
    """
    # library.properties is not JSON so I can't use my functions
    retry_count = 0
    while retry_count <= maximum_urlopen_retries:
        retry_count += 1
        url = normalize_url(url="https://raw.githubusercontent.com/" +
                                repository_object["full_name"] + "/" +
                                repository_object["default_branch"] + "/" +
                                metadata_folder +
                                "/library.properties")
        logger.info("Opening URL: " + url)
        try:
            with urllib.request.urlopen(url) as url_data:
                # step through each line of library.properties
                for line in url_data.read().decode("utf-8", "ignore").splitlines():
                    # split the line by the first =
                    field = line.split('=', 1)
                    if len(field) > 1:
                        field_name = field[0].strip()
                        field_value = field[1]

                        if field_name == "name":
                            row_list[Column.library_manager_name] = str(field_value)
                        elif field_name == "version":
                            row_list[Column.library_manager_version] = str(field_value)
                        elif field_name == "author":
                            row_list[Column.library_manager_author] = str(field_value)
                        elif field_name == "maintainer":
                            row_list[Column.library_manager_maintainer] = str(field_value)
                        elif field_name == "sentence":
                            row_list[Column.library_manager_sentence] = str(field_value)
                        elif field_name == "paragraph":
                            row_list[Column.library_manager_paragraph] = str(field_value)
                        elif field_name == "category":
                            row_list[Column.library_manager_category] = str(field_value)
                        elif field_name == "url":
                            row_list[Column.library_manager_url] = str(field_value)
                        elif field_name == "architectures":
                            row_list[Column.library_manager_architectures] = str(field_value)
            return True
        except Exception as exception:
            if not determine_urlopen_retry(exception=exception):
                return False


def parse_library_dot_json(metadata_folder, repository_object, row_list):
    """Attempt to open the file library.json from the specified folder of the repository.
    If successful at opening the file at opening the file, attempt to parse the contents, fill cells of the row with the
    data, return True (even if decoding the JSON failed). If unsuccessful at opening the file, return False.

    Keyword arguments:
    metadata_folder -- the folder of the repository containing library.json
    repository_object -- the JSON object containing the repository data
    row_list -- the list to populate with data from the parsed library.properties
    """
    url = ("https://raw.githubusercontent.com/" +
           repository_object["full_name"] + "/" +
           repository_object["default_branch"] + "/" +
           metadata_folder + "/library.json")
    try:
        get_json_from_url_return = get_json_from_url(url=url)
    except json.decoder.JSONDecodeError:
        logger.warning("Unable to decode JSON of: " + url)
        # library.json was found but could not be decoded so skip parsing but return True because the file does exist
        return True
    except (urllib.error.HTTPError, TimeoutError):
        # the file doesn't exist
        return False

    json_data = dict(get_json_from_url_return["json_data"])
    try:
        row_list[Column.platformio_name] = str(json_data["name"])
    except KeyError:
        pass
    except TypeError:
        logger.warning("Can't handle type of library.json name field for " + repository_object["html_url"])

    try:
        row_list[Column.platformio_description] = str(json_data["description"])
    except KeyError:
        pass
    except TypeError:
        logger.warning("Can't handle type of library.json description field for " + repository_object["html_url"])

    try:
        row_list[Column.platformio_keywords] = str(json_data["keywords"])
    except KeyError:
        pass
    except TypeError:
        logger.warning("Can't handle type of library.json keywords field for " + repository_object["html_url"])

    try:
        # the PlatformIO library.json specification:
        # http://docs.platformio.org/en/latest/librarymanager/config.html#authors
        # says authors can be either array (Python list) or object (Python dict)
        if type(json_data["authors"]) is list:
            row_list[Column.platformio_authors] = ", ".join(author["name"] for author in json_data["authors"])
        elif type(json_data["authors"]) is dict:
            row_list[Column.platformio_authors] = json_data["authors"]["name"]
        # just for kicks, try str
        elif type(json_data["authors"]) is str:
            row_list[Column.platformio_authors] = json_data["authors"]
        else:
            # what the heck is it?
            logger.warning("Can't handle type of library.json authors field for " + repository_object["html_url"])
    except KeyError:
        pass

    try:
        row_list[Column.platformio_repository] = str(json_data["repository"]["url"])
    except KeyError:
        pass
    except TypeError:
        logger.warning("Can't handle type of library.json repository field for " + repository_object["html_url"])

    try:
        row_list[Column.platformio_version] = str(json_data["version"])
    except KeyError:
        pass
    except TypeError:
        logger.warning("Can't handle type of library.json version field for " + repository_object["html_url"])

    try:
        row_list[Column.platformio_license] = str(json_data["license"])
    except KeyError:
        pass
    except TypeError:
        logger.warning("Can't handle type of library.json license field for " + repository_object["html_url"])

    try:
        row_list[Column.platformio_download_url] = str(json_data["downloadUrl"])
    except KeyError:
        pass
    except TypeError:
        logger.warning("Can't handle type of library.json downloadUrl field for " + repository_object["html_url"])

    try:
        row_list[Column.platformio_homepage] = str(json_data["homepage"])
    except KeyError:
        pass
    except TypeError:
        logger.warning("Can't handle type of library.json homepage field for " + repository_object["html_url"])

    try:
        # PlatformIO library.json specification says frameworks field can be either String or Array
        if type(json_data["frameworks"]) is list:
            # concatenate list items into a comma-separated string
            row_list[Column.platformio_frameworks] = ", ".join(json_data["frameworks"])
        elif type(json_data["frameworks"]) is str:
            row_list[Column.platformio_frameworks] = json_data["frameworks"]
        else:
            logger.warning("Couldn't parse library.json frameworks field for " + repository_object["html_url"])
    except KeyError:
        pass

    try:
        # PlatformIO library.json specification says platforms field can be either String or Array
        if type(json_data["platforms"]) is list:
            # concatenate list items into a comma-separated string
            row_list[Column.platformio_platforms] = ", ".join(json_data["platforms"])
        elif type(json_data["platforms"]) is str:
            row_list[Column.platformio_platforms] = json_data["platforms"]
        else:
            logger.warning("Couldn't parse library.json platforms field for " + repository_object["html_url"])
    except KeyError:
        pass

    return True


def get_repository_license(repository_object):
    """Interpret the values of the license metadata and return its SPDX ID.

    Keyword arguments:
    repository_object -- the repository's JSON
    """
    if repository_object["license"] is None:
        # no license file in the repo root
        return "none"
    elif repository_object["license"]["spdx_id"] is None:
        # there is a license file but the Licensee Ruby gem used by GitHub was unable to determine a standard license
        # type from it
        return "unrecognized"
    else:
        return repository_object["license"]["spdx_id"]


def get_contributor_count(repository_object):
    """Determine the number of contributors to the repository and return that value.

    Keyword arguments:
    repository_object -- the repository's JSON
    """
    # the GitHub API doesn't provide a contributor count, only a list of contributors
    # since I need to call get_json_from_url() directly in order to set a custom per_page value, I need to call
    # check_rate_limiting() first
    check_rate_limiting(api_type="core")
    # so the most efficient way to get the count is to set per_page=1 and then the number of pages of results will be
    # the contributor count
    try:
        get_json_from_url_return = get_json_from_url(url="https://api.github.com/repos/" +
                                                         repository_object["full_name"] +
                                                         "/contributors?per_page=1")
        return str(get_json_from_url_return["page_count"])
    except (json.decoder.JSONDecodeError, TimeoutError):
        # it's unknown under which conditions this would occur
        logger.warning("Unable to get contributor count")
        return ""


def create_output_file():
    """Do final formatting of the table. Write it as a tab separated file."""
    list_count = len(table) - 1
    print("\nNumber of libraries found: " + str(list_count))
    if list_count == 0:
        logger.warning("Canceling output file creation because the list has no libraries.")
        # no reason to write an empty file, and it might be overwriting a good one
        return

    # alphabetize table by the first column
    table.sort()

    # create the CSV file
    # if the file already exists, this will clear it of previous data
    with open(file=output_filename, mode="w", encoding="utf-8", newline='') as csv_file:
        # create the writer object
        csv_writer = csv.writer(csv_file, delimiter=output_file_delimiter, quotechar=output_file_quotechar)
        # write the table to the CSV file
        csv_writer.writerows(table)


# only execute the following code if the script is run directly, not imported
if __name__ == '__main__':
    # parse command line arguments
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("--ghtoken", dest="github_token", help="GitHub personal access token", metavar="TOKEN")
    argument_parser.add_argument("--verbose", dest="enable_verbosity", help="Enable verbose output",
                                 action="store_true")
    argument = argument_parser.parse_args()

    # run program
    main()
