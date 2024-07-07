

# Casting Agency React Application

This application is based on the [Auth0 Sample React app.](https://github.com/auth0-samples/auth0-react-samples/tree/master/Sample-01)

## Project setup

From `frontend` folder, use `yarn` to install the project dependencies:

```bash
yarn install
```

## Configuration

### Configure credentials

The project needs to be configured with your Auth0 domain and client ID in order for the authentication flow to work.

To test with your own credentials, need to update in 
`src/auth_config.json`

## Run the app

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