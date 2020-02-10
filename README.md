# sierra-pywr

Code base for modeling the central Sierra Nevada hydropower systems and implementing said models to optimize performance and 
make predictions of future scenarios

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Get your environment set up, depending on your Operating System, as well as IDE, we advise installing 
[Pywr](https://pywr.github.io/pywr-docs/master/index.html)


### Installation

A step by step series of examples that tell you how to get a development env running

#OS X & Linux:

```sh
$ sudo apt-get install libgmp3-dev libglpk-dev glpk
$ sudo apt-get install liblpsolve55-dev lp-solve
```

If you choose to use Anaconda environment for OS X or Linux:

```sh
$ wget https://repo.anaconda.com/archive/Anaconda3-2019.03-Linux-x86_64.sh
```
Remove the installation file:
```sh
$ rm Anaconda3-2019.03-Linux-x86_64.sh
```
Update Anaconda:

```sh
$ source ~anaconda3/bin/activate
$ conda update --all
```

#Windows:

1. Install Anaconda Environment [here](https://www.anaconda.com/distribution/#download-section)
2. Create new environment
3. Install the necessary packages (Pywr)
4. Setup $PATH under environment manager
5. Import your environment into your IDE

## Running the Models 

For only daily models:

```
conda activate *environment_name*
python main.py -b *network* -n "development" -d d
```
For both daily and monthly models

```
conda activate *environment_name*
python main.py -b *network* -p -n "development" -d dm
```

## Setting Up Models in Merced Cluster

1. Request an account [here](http://hpcwiki.ucmerced.edu/knowledgebase/getting-a-merced-account) for access to the cluster
2. Access the UC Merced VPN via Cisco Anyconnect, 

[Windows Setting up](https://ucmerced.service-now.com/kb_view.do?sysparm_article=KB0010636) \
[Windows Connecting](https://ucmerced.service-now.com/kb_view.do?sysparm_article=KB0010500) \
[Linux Setting up](https://ucmerced.service-now.com/kb_view.do?sysparm_article=KB0010634) \
[Linux Connecting](https://ucmerced.service-now.com/kb_view.do?sysparm_article=KB0010499)

3. Using a linux terminal:
```sh

$ ssh <username>@merced.ucmerced.edu   
```
4. Once logged in, check to see what content is available.

```sh

$ ls
help data scratch
```
In order to execute jobs, the cluster uses a workload manager called [Slurm](https://slurm.schedmd.com/)

5. Run a test job in the cluster using one of the files under the help section, in this case: projectile.exe

```sh

$ vim projectile.exe
```
Looking at the #SBATCH scripts, the following is what is standard usage for running tasks in the cluster. Any more, and there could be issues such as potentially getting your account revoked.

```sh
 #SBATCH --nodes=1
 #SBATCH --ntasks=1
 #SBATCH --cpus-per-task=1
 #SBATCH --mem-per-cpu=1G
 #
 #SBATCH --partition fast.q 
 #SBATCH --time=0-00:15:00     # 0days 15 minutes
 #
 #SBATCH --output=myjob_%j.stdout
 #
 #SBATCH --job-name=test
 #SBATCH --export=ALL
```
6. After analyzing the code, you can run it via these commands on the termninal:

```sh

$ cp ~/help/projectile.exe ~/
$ cp ~/help/sample.sub ~/
```

7. Setup Modules for your environment:

* module avail - lists all modules
* module_load <mod_name> - loads the environment based on <mod_name>
* module list - provides a list of all modules currently loaded into the user environment. 
* module unload <mod_name> - unloads the environment corresponding to <mod_name>.
* module swap <mod_1> <mod_2> - unloads the environment corresponding to <mod_1> and loads that corresponding to <mod_2>.

For more information, check the [Merced Cluster User Manual](http://hpcwiki.ucmerced.edu/knowledgebase/merced-cluster-user-manual/)

## Built With

* [Pywr](https://pywr.github.io/pywr-docs/master/index.html) - The main library used
* [Python Flask](https://maven.apache.org/) - Dependency Management

## Authors

* **David Rheinheimer** - [rheinheimer](https://github.com/rheinheimer)
* **Aditya Sood** - [asood12](https://github.com/asood12)
* **Dan Tran** - [GateauXD](https://github.com/GateauXD)
* **Lorenzo Scaturchio** - [gr8monk3ys](https://github.com/gr8monk3ys)

See also the list of [contributors](https://github.com/vicelab/sierra-pywr/contributors) who participated in this project.