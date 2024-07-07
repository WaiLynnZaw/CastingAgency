#!/bin/bash
export AUTH0_DOMAIN='dev-a2hj2l3zh36odzdo.us.auth0.com'
export ALGORITHMS=['RS256']
export API_AUDIENCE='casting-agency'
export DATABASE_URL='postgresql://localhost:5432/casting-agency'
export DATABASE_URL_TEST='postgresql://localhost:5432/casting-agency-test'

echo $AUTH0_DOMAIN
echo $ALGORITHMS
echo $API_AUDIENCE
echo $DATABASE_URL
echo $DATABASE_URL_TEST
