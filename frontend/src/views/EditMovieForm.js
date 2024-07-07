import React, { useState, useEffect } from 'react';
import Swal from 'sweetalert2';
import { useAuth0, withAuthenticationRequired } from '@auth0/auth0-react';
import { getConfig } from '../config';
import { useHistory, useParams } from 'react-router-dom';
import usePermissions from '../utils/permissions';
import Loading from "../components/Loading";

export const EditMovieForm = () => {
  const { apiOrigin = "https://casting-agency-api-v0sn.onrender.com" } = getConfig();
  const { getAccessTokenSilently } = useAuth0();
  const { hasPermission } = usePermissions();
  const history = useHistory();
  const { id } = useParams();
  
  const [title, setTitle] = useState('');
  const [releaseDate, setReleaseDate] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMovie = async () => {
      try {
        const token = await getAccessTokenSilently();
        const response = await fetch(`${apiOrigin}/movies/${id}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const movie = await response.json();
        setTitle(movie.movie.title);
        setReleaseDate(movie.movie.release_date);
        setLoading(false);
      } catch (error) {
        Swal.fire({
          icon: 'error',
          title: 'Error!',
          text: 'There was an error fetching the movie data.',
          showConfirmButton: true,
        });
        setLoading(false);
      }
    };

    fetchMovie();
  }, [id, apiOrigin, getAccessTokenSilently]);

 

  const handleEdit = async (e) => {
    e.preventDefault();

    if (!hasPermission('patch:movie')) {
      return Swal.fire({
        icon: 'error',
        title: 'Unauthorized!',
        text: 'You do not have permission to edit this movie.',
        showConfirmButton: true,
      });
    }

    if (!title || !releaseDate) {
      return Swal.fire({
        icon: 'error',
        title: 'Error!',
        text: 'All fields are required.',
        showConfirmButton: true,
      });
    }

    try {
      const token = await getAccessTokenSilently();
      await fetch(`${apiOrigin}/movies/${id}`, {
        method: "PATCH",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ title, release_date: releaseDate }),
      });

      Swal.fire({
        icon: 'success',
        title: 'Updated!',
        text: `${title} has been updated.`,
        showConfirmButton: false,
        timer: 1500,
      });

      history.push('/movies');
    } catch (error) {
      Swal.fire({
        icon: 'error',
        title: 'Error!',
        text: 'There was an error updating the movie.',
        showConfirmButton: true,
      });
    }
  };

  // if (loading) {
  //   return <div>Loading...</div>;
  // }

  return (
    <div className="small-container">
      <form onSubmit={handleEdit}>
        <h1>Edit Movie</h1>
        <label htmlFor="title">Title</label>
        <input
          id="title"
          type="text"
          name="title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <label htmlFor="releaseDate">Release Date</label>
        <input
          id="releaseDate"
          type="date"
          name="releaseDate"
          value={releaseDate}
          onChange={(e) => setReleaseDate(e.target.value)}
        />
        <div style={{ marginTop: '30px' }}>
          <input type="submit" value="Update" />
          <input
            style={{ marginLeft: '12px' }}
            className="muted-button"
            type="button"
            value="Cancel"
            onClick={() => history.push('/movies')}
          />
        </div>
      </form>
    </div>
  );
};

export default withAuthenticationRequired(EditMovieForm, {
  onRedirecting: () => <Loading />,
});