# Static Site Generator

> This is a project from [boot.dev](https://www.boot.dev/tracks/backend)'s backend track creating a static site generator using python

## How to run the project

To start the project
```shell
./main.sh
```

If you are using a unix based operating system run this command first
```linux
chmod +x ./main.sh
```

The generator only convert *markdown* files which are located in the `/content` folder.
Other file extensions are ignored altogether.

Image resources which are used in the `markdown` files should be included in the `/static` folder.
