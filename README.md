# Introduction

ComodIT client is both a Python library to interact with ComodIT's API and
a Command-Line Interface (CLI) to ComodIT. The CLI actually relies on the
library when querying the server. In addition to common operations
(creation, update and deletion) on ComodIT entities, library and CLI provide additional
tools: import/export facilities as well as a sync engine allowing to synchronize
ComodIT entities with a local folder (see last section).

The CLI features a man page and dynamic (i.e. based on remote data fetched in
real-time) auto-completion (at least with shells supporting bash completions
system).

Below you will find usage examples for both CLI and library. These examples
suppose that you already have a ComodIT account. If it is not yet the case, do
not hesitate to [register](https://my.comodit.com/), it's free!


# Command-Line Interface

## Configuration

Configuring the client is not mandatory but exempts you to provide your
connection credentials on each call to the client. However, keep in mind
that configuration file will contain your credentials in plain text. Therefore,
set your permissions accordingly or do not use this feature if you are not in a
"safe environment".

CLI's per-user configuration is stored in file '~/.comoditrc'. You may set
its content as follows:

    [client]
    default_profile = default

    [default]
    api = https://my.comodit.com/api
    username = UUU
    password = PPP
    vnc_viewer_call = vinagre %h:%p

where *UUU* and *PPP* are respectively your ComodIT username and password.
*vnc\_viewer\_call* should be set in function of your default VNC client (if you
plan to use this feature).


## Quickstart

For the sake of readability, we consider in the following that you configured
your client as described in above section. If you chose not to configure your
client, do not forget to use options *--api*, *--user* and *--pass* to provide
API's URL, username and password to the client.

1. Change directory to client's directory.
2. If you have a bash-like shell, enable auto-completion by sourcing
'auto_completion/comodit' file (this is optional).
3. List ComodIT's organizations you have access to on [my.comodit.com](https://my.comodit.com/) by executing
the following command:

        ./comodit organizations list

    where UUU and PPP are respectively your username and password.
4. Show one of these organizations by executing the following command:

        ./comodit organizations show OOO

    where OOO is a name that was displayed at step 3. You should see something
    like this:
    
        Name: OOO
        Description: 
        Access Key: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        Secret Key: YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY
        Environments:
          Default
        Groups:
          users
          admin
          readonly

    If you are already familiar with ComodIT, these informations should be
    self-explanatory. If it is not the case, please have a look at
    [ComodIT's documentation](http://www.comodit.com/resources/)
    before you go further.

5. Create a host in 'Default' environment of step 4's organization:

        ./comodit hosts add OOO Default

    This command should open a JSON representation of your new host with your
    default text editor. Change it to obtain something like this:

        {
            "name": "my-new-host",
            "platform": "Demo Platform",
            "settings": [
            ],
            "environment": "Default",
            "applications": [
            ],
            "organization": "OOO",
            "distribution": "Demo Distribution",
            "description": "My new host."
        }

    *organization* and *environment* fields have been pre-filled. *Demo Platform*
    and *Demo Distribution* are available by default when you create a new
    organization in my.comodit.com.

    Save the file and close the editor, you should then obtain the following
    output:

        Name: my-new-host
        Description: My new host.
        Organization: OOO
        Environment: Default
        Platform: Demo Platform
        Distribution: Demo Distribution
        State: DEFINED

6. Provision your new host:

        ./comodit hosts provision OOO Default my-new-host

7. You can now check that your host's state has changed:

        ./comodit hosts show OOO Default my-new-host

    which outputs the following lines:

        Name: my-new-host
        Description: My new host.
        Organization: OOO
        Environment: Default
        Platform: Demo Platform
        Distribution: Demo Distribution
        State: PROVISIONING

8. Re-execute command from step 7 after a minute or two, state should have
switched from *PROVISIONING* to *READY*. This means your host has been successfully
provisioned. You may now display information related to its instance by
executing the following command:

        ./comodit hosts instance show OOO Default my-new-host

    which gives an output similar to:

        State: RUNNING
        Agent state: Up
        Hostname: None
        Vnc:
          hostname: ...
          port: 5901

    where you can essentially see that 1) your instance is running and 2) that the agent
    installed on it is up and running.

9. Install application *Wordpress* (available by default in your new organization)
on your newly provisioned host:

        ./comodit hosts applications install OOO Default my-new-host Wordpress

    This command opens a JSON representation of an application context. Change
    it to obtain something like this:

        {
            "application": "Wordpress",
            "settings": [
                {
                    "key": "wp_admin_password",
                    "value": "XXX"
                },
                {
                    "key": "wp_admin_email",
                    "value": "YYY@ZZZ"
                }
            ]
        }

    where *XXX* is the admin password for installed wordpress blog and *YYY@ZZZ*
    admin's e-mail address.

10. See if there are still pending changes related to the installation:

        ./comodit hosts changes list OOO Default my-new-host

    Once the message 'No entities to list' is displayed, your Wordpress blog
    should be up and running.

11. Get the public DNS name of your instance:

        ./comodit hosts instance properties OOO Default my-new-host

    Copy the value of property with key *publicDnsName* to your browser, you
    should have access to your blog.

12. You may now tear down your host's instance by executing the following command:

        ./comodit hosts instance delete OOO Default my-new-host

    Note that your host is still defined (as at the end of step 5). If you want
    to delete the host itself, execute the following command:

        ./comodit hosts delete OOO Default my-new-host

For more details about CLI usage, please see man page (see next section).


## Documentation

The CLI is documented by a man page ('doc/comodit.1' file). You can read it by
executing the following command:

    man doc/comodit.1

A [tutorial](http://www.comodit.com/resources/tutorials/cli.html) is also
available on ComodIT's documentation page.


# Python Library

## Quickstart

The following script does essentially the same as the procedure exposed in
CLI's quickstart section:

    from comodit_client.api import Client

    # Connect to ComodIT
    client = Client('https://my.comodit.com/api', 'UUU', 'PPP')

    # Create host
    org = client.get_organization('OOO')
    host = org.get_environment('Default').hosts().create('my-new-host', '', 'Demo Platform', 'Demo Distribution')

    # Provision host
    host.provision()
    host.wait_for_state('READY')

    # Install an application
    host.install('Wordpress', {'wp_admin_password': 'XXX', 'wp_admin_email': 'YYY@ZZZ'})
    host.wait_for_pending_changes()

    # Retrieve instance's hostname
    hostname = host.get_instance().get_property('publicDnsName')
    print "Wordpress available at http://" + hostname + "/"

    # Delete host and its instance
    host.get_instance().delete()
    host.delete()

If you want to reuse above code, do not forget to replace *UUU*, *PPP*, *OOO*, *XXX*
and *YYY@ZZZ* by real values. Also be sure to have a Python path correctly set up.
For more details about library usage, please see documentation (see next
section).


## Documentation

The library's documentation is embedded in source code.
However, an HTML version can be generated by executing the following command (you must
have Epydoc installed on your computer):

    ./scripts/build-doc.sh

If the script executed itself successfully, open the following file with your browser:
'doc/html/index.html'.


# Advanced: Import, Export and Synchronization

Currently, ComodIT's entities are managed through WEB interface or CLI. However,
in some situations, it may be convenient to save some entities onto disk, for
backup purposes or simply to move an entity (application, platform or distribution)
from one organization to another. Another interesting use case is version
control for recipes you've written: you develop and test your applications
with the WEB
interface but want to keep track of the alterations; to do so, you regularly
synchronize the applications representation on disk in a directory that is
version controlled, with entities from the server.

All these use-cases can be addressed using import, export or synchronization
tool, or a combination of them. They are exposed below.

## Representation on Disk

An entity is represented on disk by a folder containing at least one file called
'definition.json' which contains the JSON representation of the entity.
If the entity (applications and distributions) has a thumbnail,
the folder also contains a file called 'thumb' (this file can contain any type
of image supported by most browsers). Finally, if the entity owns a collection,
a folder containing collections' entities representations (one folder per
entity) is created. Settings, files and parameters collections do not require
additional folders because their definition is embedded in owning entity's
representation. However, files still require a 'files' folder containing one
file per file entity, each file containing the content of associated file entity.

For instance, a distribution exported to disk may imply the following
directory structure:

- definition.json
- thumb
- files/
  - kickstart.cfg

where *kickstart.cfg* is the name of distribution's single file and contains the
kickstart template.

## Use-cases

### Backup/move an application, distribution or platform

1. Export target entity onto disk by using 'export' action. For instance,
to export application *A* from organization *O* into folder *D*, execute the
following command:

        ./comodit applications export O A D

2. Import source entity from disk by using 'import' action. For example, to
import an application previously exported to directory *D* into organization *Q*,
execute the following command:

        ./comodit applications import Q D

### Version an application's recipe

1. Initially, export the application *A* of organization *O* to a version
controlled directory *D* (see previous section).

2. Commit exported files.

3. Apply changes to application and test it with ComodIT.

4. Synchronize local representation with server using sync engine's 'pull' action:

        ./comodit applications sync pull O A D

    Before actually synchronizing, you may want to review the operations that
    will be executed; to do so, use --dry-run option.

5. Go back to step 3.

In some rare cases, you may want to develop you application directly by modifying
files on your disk, then upload your changes onto the server. The process then
becomes:

1. Initially, export the application *A* of organization *O* to a version
controlled directory *D* (see previous section).

2. Commit exported files.

3. Apply changes to your files.

4. Synchronize server with local representation using sync engine's 'push' action:

        ./comodit applications sync push O A D

    Before actually synchronizing, you may want to review the operations that
    will be executed; to do so, use --dry-run option.

5. Test your application and go back to step 3.
