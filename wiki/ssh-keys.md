# SSH Keys

Ssh keys are useful in allowing a user to login to a remote device without having to enter a password. Ssh keys can be configured to request an additional passphrase, but since we are not concerned with security, we will not be using this feature. Ssh keys consist of a private and public key (a pair of files) which are used to authenticate users. The private key is stored on the *remote user's* machine (and not to be shared), whereas the public key is deployed to *servers*. In this case, the *PC* is the remote user and the *Raspberry Pi* would be considered the server.

Since we are automating the process of data collection, we want to take advantage of this ability to run the script on the Raspberry Pi without user intervention/ authentication.

***

## Generate the Keys

To generate a pair of ssh keys, on the remote user's machine run the `ssh-keygen` command. On Windows, this can be done through the command line or powershell. Go through the prompts that follow. I would recommend renaming the file to be something descriptive. Leave the passphrase prompt blank. Once complete, the ssh public and private keys will have been created and stored in the supplied directory. On Windows, ssh keys are typically stored in `C:\Users\<username>\.ssh`. Again, this process creates two files. The public key will have a `.pub` extension and the one with no extension is the private key. The private key will remain on the Windows PC and the public `.pub` file will need to be transferred to the Raspberry Pi.&#x20;

***

## Transfer the Keys

To make use of the ssh-key, we need to transfer the ***public key*** to the *server*, in this case the Raspberry Pi. On Linux, ssh keys are stored in `/home/user/.ssh`. Transfering the file can simply be done by copying the file over using a USB drive. If the Raspberry Pi is connected to a Windows PC using *gadget mode*, this can also be done using the following command:

```bash
scp C:\Users\<username>\.ssh\ssh-public-key.pub pi@raspberrypi.local:/home/pi/.ssh

# more generally
scp C:\path\to\ssh-public-key.pub user@hostname.local:/home/user/.ssh
```

You will be prompted for the user's password. Of course, modify the command with the appropriate file names, usernames, and hostname of the Raspberry Pi, if it has been changed. This will store the public key in `/home/user/.ssh` on the Raspberry Pi.

***

## Add the Public Key to authorized_keys

On the server, or the Raspberry Pi, create a file called `authorized_keys` in `/home/user/.ssh`. We simply need to copy the contents of the public key file into the authorized keys file. This can be done using (modifying the file name as needed):

```bash
cat /home/user/.ssh/ssh-public-key.pub >> /home/user/.ssh/authorized_keys
```

***

## Permissions

Before continuing, we need to set the correct permissions on the `authorized_keys` file. The permissions should be set to 644 and the user should own the file. To set the permissions, on the Raspberry Pi, run the following:

```bash
sudo chmod 644 /home/user/.ssh/authorized_keys
```

***

## Logging In

Finally, to ssh in to the Raspberry Pi (in gadget mode) from a Windows PC, we need to specify the private key file using the `-i` option:

    ssh -i C:\Users\<username>\.ssh\ssh-private-key user@hostname.local

If it logs in without a password prompt, then the ssh keys are all set.&#x20;

***