/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'fsndcoffeeapi.eu.auth0.com', // the auth0 domain prefix
    audience: 'http://127.0.0.1:5000', // the audience set for the auth0 app
    clientId: 'PcKe59jeESa3IR7Iy9Umd3dL31MjyK7Q', // the client id generated for the auth0 app
    callbackURL: 'http://127.0.0.1:8100', // the base url of the running ionic application.
  },
};
