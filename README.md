# Dear Future Matt

To reupload:

* Run local to get a session
* docker build -t tgramphotos .
* docker save tgramphotos | gzip > tgramphotos.tar.gz
* Keep the SESSION there, or it wont work.
* When creating running docker, go to environmental vars, and add everything from .env
* This gives you full control over the running instance
