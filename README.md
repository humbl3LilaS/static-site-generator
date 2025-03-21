# Static Site Generator

> This is a project from [boot.dev](https://www.boot.dev/tracks/backend)'s backend track creating a static site generator using python

## How to run the project

to start the project
```shell
./main.sh
```

if you are using a unix based operating system run this command first
```linux
chmod +x ./main.sh
```

The generator only convert *markdown* file which are located in the `/content` folder.
Other file extension are ignored altogether.

Image resources which will are used in the `markdown` file should be included in the `/static` folder.