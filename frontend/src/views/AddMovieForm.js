import React, { useState } from 'react';
import Swal from 'sweetalert2';
import { useAuth0, withAuthenticationRequired } from '@auth0/auth0-react';
import { getConfig } from '../config';
import { useHistory } from 'react-router-dom';
import usePermissions from '../utils/permissions';
import Loading from "../components/Loading";
import authConfig from "../auth_config.json"
export const AddMovieForm = () => {
  const { apiOrigin = authConfig.baseUrl } = getConfig();
  const { getAccessTokenSilently } = useAuth0();
  const { hasPermission } = usePermissions();
  const history = useHistory();

  const [title, setTitle] = useState('');
  const [releaseDate, setReleaseDate] = useState('');

  const handleAdd = async (e) => {
    e.preventDefault();

    if (!hasPermission('post:movies')) {
      return Swal.fire({
        icon: 'error',
        title: 'Unauthorized!',
        text: 'You do not have permission to add a new movie.',
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
      const response = await fetch(`${apiOrigin}/movies`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ title, release_date: releaseDate }),
      });

      // const responseData = await response.json();

      Swal.fire({
        icon: 'success',
        title: 'Added!',
        text: `${title} has been added.`,
        showConfirmButton: false,
        timer: 1500,
      });

      setTitle('');
      setReleaseDate('');
      history.push('/movies');
    } catch (error) {
      Swal.fire({
        icon: 'error',
        title: 'Error!',
        text: 'There was an error adding the movie.',
        showConfirmButton: true,
      });
    }
  };

  return (
    <div className="small-container">
      <form onSubmit={handleAdd}>
        <h1>Add Movie</h1>
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
          <input type="submit" value="Add" />
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

export default withAuthenticationRequired(AddMovieForm, {
  onRedirecting: () => <Loading />,
});