## Project setup

Use `yarn` to install the project dependencies:

```bash
yarn install
```

## Configuration

### Build an API

For the ["call an API"](https://auth0.com/docs/quickstart/spa/react/02-calling-an-api) page to work, you will need to [create an API](https://auth0.com/docs/apis) using the [management dashboard](https://manage.auth0.com/#/apis). This will give you an API identifier that you can use in the `audience` configuration field below.

If you do not wish to use an API or observe the API call working, you should not specify the `audience` value in the next step. Otherwise, you will receive a "Service not found" error when trying to authenticate.

### Defined credentials

The project must be signed in with the below credential which are pre-defined users for the testing purpose.

`Executive Producer`
```
producer@gmail.com
Producer2024
```

`Director`
```
director@gmail.com
Director2024
```

`Assistant`
```
assistant@gmail.com
Assistant2024
```

**Note**: Do not specify a value for `audience` here if you do not wish to use the API part of the sample.

## Run the sample

### Compile and hot-reload for development

This compiles and serves the React app and starts the backend API server on port 3001.

```bash
yarn run dev
```

## Deployment

### Compiles and minifies for production

```bash
yarn run build
```

### Run your tests

```bash
yarn run test
```
