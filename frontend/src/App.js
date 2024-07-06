import React from "react";
import { Router, Route, Switch } from "react-router-dom";
import { Container } from "reactstrap";
import { useAuth0 } from "@auth0/auth0-react";
import history from "./utils/history";

import Loading from "./components/Loading";
import NavBar from "./components/NavBar";
import Home from "./views/Home";
import Profile from "./views/Profile";
import Movie from "./views/Movie";
import AddMovieForm from './views/AddMovieForm'; // Import AddMovieForm
import EditMovieForm from './views/EditMovieForm'; // Import EditMovieForm
import Actor from "./views/Actor";
import AddActorForm from './views/AddActorForm';
import EditActorForm from './views/EditActorForm';

// styles
import "./App.css";

// fontawesome
import initFontAwesome from "./utils/initFontAwesome";
initFontAwesome();

const App = () => {
  const { isLoading, error } = useAuth0();

  if (error) {
    return <div>Oops... {error.message}</div>;
  }

  if (isLoading) {
    return <Loading />;
  }

  return (
    <Router history={history}>
      <div id="app" className="d-flex flex-column h-100">
        <NavBar />
        <Container className="flex-grow-1 mt-5">
          <Switch>
            <Route path="/" exact component={Home} />
            <Route path="/profile" component={Profile} />
            <Route path="/movies" component={Movie} />
            <Route path="/add-movie" component={AddMovieForm} />
            <Route path="/edit-movie/:id" component={EditMovieForm} /> {/* Add route for EditMovieForm */}
            <Route path="/actors" component={Actor} />
            <Route path="/add-actor" component={AddActorForm} />
            <Route path="/edit-actor/:id" component={EditActorForm} />
          </Switch>
        </Container>
        {/* <Footer /> */}
      </div>
    </Router>
  );
};

export default App;
