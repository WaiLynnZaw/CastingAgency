import React, { useEffect, useState, useCallback } from 'react';
import Swal from 'sweetalert2';
import { useAuth0, withAuthenticationRequired } from '@auth0/auth0-react';
import { getConfig } from '../config';
import { useHistory } from "react-router-dom";
import usePermissions from '../utils/permissions';
import Loading from "../components/Loading";

export const MovieComponent = () => {
  const { apiOrigin = 'https://casting-agency-api-v0sn.onrender.com' } = getConfig();
  const { getAccessTokenSilently } = useAuth0();
  const { hasPermission } = usePermissions();
  const [movies, setMovies] = useState([]);
  const history = useHistory();

  const fetchMovies = useCallback(async () => {
    try {
      const token = await getAccessTokenSilently();
      const response = await fetch(`${apiOrigin}/movies`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      const data = await response.json();
      setMovies(data.movies);
    } catch (error) {
      console.error('Error fetching movies:', error);
    }
  }, [apiOrigin, getAccessTokenSilently]);

  useEffect(() => {
      fetchMovies();
  }, [fetchMovies]);

  const handleDeleteMovie = async (id) => {
    if (!hasPermission('delete:movie')) {
      return Swal.fire({
        icon: 'error',
        title: 'Error!',
        text: 'You do not have permission to delete a movie.',
        showConfirmButton: true,
      });
    }
    const result = await Swal.fire({
      icon: 'warning',
      title: 'Are you sure?',
      text: "You won't be able to revert this!",
      showCancelButton: true,
      confirmButtonText: 'Yes, delete it!',
      cancelButtonText: 'No, cancel!',
    });

    if (result.isConfirmed) {
      try {
        const token = await getAccessTokenSilently();
        await fetch(`${apiOrigin}/movies/${id}`, {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        Swal.fire(
          'Deleted!',
          'The movie has been deleted.',
          'success'
        );
        setMovies(movies.filter((m) => m.id !== id));
      } catch (error) {
        Swal.fire({
          icon: 'error',
          title: 'Error!',
          text: 'There was an error deleting the movie.',
          showConfirmButton: true,
        });
      }
    }
  };

  return (
    <div className="container">
      <h1>Movies</h1>
      <div style={{ marginBottom: '18px' }}>
        {hasPermission('post:movies') && (
          <button onClick={() => history.push('/add-movie')}>Add Movie</button>
        )}
      </div>
      <div className="contain-table">
        <table className="striped-table">
          <thead>
            <tr>
              <th>No.</th>
              <th>Title</th>
              <th>Release Date</th>
              <th colSpan={2} className="text-center">
                Actions
              </th>
            </tr>
          </thead>
          <tbody>
            {movies.length > 0 ? (
              movies.map((movie, i) => (
                <tr key={movie.id}>
                  <td>{i + 1}</td>
                  <td>{movie.title}</td>
                  <td>{movie.release_date}</td>
                  <td className="text-right">
                    {hasPermission('patch:movie') && (
                      <button
                        onClick={() => history.push(`/edit-movie/${movie.id}`)}
                        className="button muted-button"
                      >
                        Edit
                      </button>
                    )}
                  </td>
                  <td className="text-left">
                    {hasPermission('delete:movie') && (
                      <button
                        onClick={() => handleDeleteMovie(movie.id)}
                        className="button muted-button"
                      >
                        Delete
                      </button>
                    )}
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                  <td colSpan={7} className="text-center">No Movie found</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default withAuthenticationRequired(MovieComponent, {
  onRedirecting: () => <Loading />,
});
