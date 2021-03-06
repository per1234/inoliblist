An list of thousands of [Arduino](http://arduino.cc) library GitHub repositories with relevant metadata.


### Available list formats
- [Sortable and searchable web front end](https://per1234.github.io/inoliblist/) (slow)
- [Tab separated file](https://per1234.github.io/inoliblist/inoliblist.csv)


### List Sources
- [Arduino Library Manager index](http://downloads.arduino.cc/libraries/library_index.json)
- [GitHub's `arduino-library` topic](https://github.com/search?q=topic:arduino-library+fork:true&type=Repositories)
- [GitHub's `arduino` topic](https://github.com/search?q=topic:arduino+fork:true&type=Repositories)
  - To ensure it contains an Arduino Library, the repository must have one of the following:
    - Library metadata file ([library.properties](https://github.com/arduino/Arduino/wiki/Arduino-IDE-1.5:-Library-specification#library-metadata) or [library.json](http://docs.platformio.org/en/latest/librarymanager/config.html)).
    - A folder containing a header file (.h, .hh, .hpp) and no sketch file (.ino, .pde).
    - A folder containing a header file and either an examples folder or keywords.txt if a sketch file is present.
  - If only standard administrative files are found in the root folder then one level of subfolders is searched.
- [GitHub search for `arduino library topics:0 language:cpp language:c language:arduino fork:false`](https://github.com/search?q=arduino+library+topics:0+language:cpp+language:c+language:arduino+fork:false&type=Repositories)
  - The same library verification requirements as the `arduino` topic search.


### List Columns
- **Repository URL**
- **Owner**
- **Repo Name**
- **Default Branch**: Default branch of the repository.
- **Library Path**: The folder of the repository where a library was detected. The script only scans the repository root, and one subfolder down. If a library is not found at those locations then the field will be left empty.
- **Archived**: Whether the repository is [archived](https://help.github.com/articles/about-archiving-repositories/). Archived repositories are read-only.
- **Fork**: Whether the repository is a fork.
- **Fork Of**: If the repository is a fork, the name of the parent.
- **Last Push**: Timestamp of the last push to the repository.
- **#Forks**: Number of forks of the repository. Note: This is forks of the repository specifically, as opposed to the "Fork" number shown on a repository's GitHub homepage, which is the total number of forks in the repository's network.
- **#Stars**: Number of people who have "starred" the repository.
- **#Contributors**: Number of people who have committed to the repository. Note: This doesn't always match the contributor count shown on the home page of GitHub repositories. It may be that number includes the contributors with private email addresses.
- **Status**: Combined status of the latest commit to the default branch. Status will typically indicate the result of continuous integration checks.
- **License**: Repository license as [detected by GitHub](https://help.github.com/articles/licensing-a-repository/) from a license file in the root of the repository. Note: This does not necessarily guarantee all content in the repository has that license.
  - `none`: There is no license file.
  - `unrecognized: There is a license file but it did not match a standard license type.
- **Language**: The primary programming language of the repository, as detected by GitHub.
- **Repo Description**: The repository description, as shown at the top of its home page.
- **GitHub Topics**: The repository's [topics](https://help.github.com/articles/about-topics/).
- **In Library Manager**: Whether the repository is listed in the [Arduino Library manager index](https://github.com/arduino/Arduino/wiki/Library-Manager-FAQ).
- **LM name**: Value of the `name` field found in the library.properties metadata file used by the Arduino IDE. Note: These values are taken from the tip of the repository's default branch, not from the [Arduino Library Manager index file](http://downloads.arduino.cc/libraries/library_index.json), which populates them only from tagged versions. You can find more information on these fields in the [Arduino Library Specification](https://github.com/arduino/Arduino/wiki/Arduino-IDE-1.5:-Library-specification#libraryproperties-file-format).
- **LM version**
- **LM author**
- **LM maintainer**
- **LM sentence**
- **LM paragraph**
- **LM category**
- **LM url**
- **LM architectures**
- **PIO name**: Value of the `name` field found in the library.json metadata file used by PlatformIO. Note: These values are taken from the tip of the repository's default branch, not from the PlatformIO Library Registry. You can find more information on these fields in the [library.json documentation](http://docs.platformio.org/en/latest/librarymanager/config.html).
- **PIO description**
- **PIO keywords**
- **PIO authors**
- **PIO repository**
- **PIO version**
- **PIO license**
- **PIO downloadUrl**
- **PIO homepage**
- **PIO frameworks**
- **PIO platforms**


### List generation
The list is generated by a Python script: inoliblist.py

#### Script command line options
##### `--help`: Display available command line options for the script.
##### `--ghtoken`: GitHub Personal Access Token. The GitHub API does less strict [rate limiting](https://developer.github.com/v3/#rate-limiting) for authenticated requests. You can create a token by at this GitHub settings page: https://github.com/settings/tokens
##### `--verbose`: Enable verbose output, for debugging.


### Contributing
Pull requests or issue reports are welcome! Please see the [contribution rules](https://github.com/per1234/inoliblist/blob/master/.github/CONTRIBUTING.md) for instructions.

If this list would be more useful to you with some additional data field then feel free to open an issue report with your request and I'll see if it can be accommodated.
