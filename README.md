# SimpleCDN

A simple CDN service for your website.

### Quick Start

Use this command to get SimpleCDN up and running in Docker:

```bash
docker run -td \ 
    --restart unless-stopped \
    -p 8080:8080 \
    -v FILES_DIR:/data \
    --name cdn \
    karx/simplecdn:latest
```

Change the above example as needed.

## Running in Docker

This container uses a popular port used commonly for webservers, 8080. **This means that this may conflict with existing applications.**

However, if you keep it at the default 8080, you will not be able to access the application through a web browser without specifying the port number.
If this is not what you want, use a reverse proxy service like Træfik or Nginx.

| Docker Arguments | Description |
| ---------------- | ----------- |
| `-p <Host Port>:<Container Port>` **Required** | Map an outside port to the containter. The Container Port should always be 8080, otherwise you will not be able to access SimpleCDN,
| `--restart unless-stopped` **Recommended** | Automatically (re)start SimpleCDN at boot or in the case of a crash.
| `-v <File Directory>:/data` **Required** | Allows SimpleCDN to write authentication data and files to the host disc. Omitting this option will lead to data loss.
| `--name cdn` *Optional* | Explicitly sets the name of the container.

If you use a Host Port other than 80, you will have to specify the port number you chose in the browser address bar, or forward requests to it using a reverse proxy like Træfik or Nginx.

## User Feedback

Please report issues on the [Github Issue Tracker](https://github.com/karx1/simplecdn). If you see an issue in the codebase or any of the documentation that you would like to fix, feel free to make a Pull Request.