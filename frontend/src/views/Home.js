import React from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import { Redirect } from 'react-router-dom';

const Home = () => {
  const { isAuthenticated } = useAuth0();

  // If the user is authenticated, redirect to the Dashboard
  if (isAuthenticated) {
    return <Redirect to="/movies" />;
  }

  return (
    <div className="container">
      <header className="header">
        <h1>Welcome to Movie and Actor Agency</h1>
        <p>
          Welcome to our Movie and Actor Agency! We manage a diverse portfolio of movies and talented actors. Browse our collection and get to know the amazing work we do in the film industry.
        </p>
      </header>
      <main className="main-content">
        <section>
          <h2>Latest News</h2>
          <p>
            Stay tuned for the latest updates and news about our latest projects and actors.
          </p>
        </section>
      </main>
    </div>
  );
};

export default Home;