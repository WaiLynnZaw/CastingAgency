import React from "react";
import { Container, Row, Col } from "reactstrap";

import Highlight from "../components/Highlight";
import Loading from "../components/Loading";
import { useAuth0, withAuthenticationRequired } from "@auth0/auth0-react";

export const ProfileComponent = () => {
  const { user } = useAuth0();

  return (
    <Container className="mb-5">

      <Row className="align-items-center profile-header mb-5 text-center text-md-left">
        <Col md={2}>
          <img
            src={user.picture}
            alt="Profile"
            className="rounded-circle img-fluid profile-picture mb-3 mb-md-0"
          />
        </Col>
        <Col md>
          <h2>{user.name}</h2>
          <p className="lead text-muted">{user.email}</p>
        </Col>
      </Row>
      <Row className="mb-5">
        <Col>
          <h3>Roles and Responsibilities</h3>
          <p><strong>Producer:</strong> As a producer, I oversee the film's production from start to finish, ensuring that the project stays on schedule and within budget. I coordinate with directors, writers, and other key personnel to bring the script to life.</p>
          <p><strong>Director:</strong> In my role as a director, I translate the script into a visual narrative, guiding actors and crew to achieve the desired vision. My goal is to tell a compelling story that resonates with the audience.</p>
          <p><strong>Assistant:</strong> As an assistant, I provide crucial support to the production team, handling various administrative tasks and ensuring smooth operations on set. This role requires multitasking and excellent organizational skills.</p>
        </Col>
      </Row>
      <Row className="mb-5">
        <Col>
          <h3>Notable Projects</h3>
          <ul>
            <li><em>The Journey</em> (Producer) - A critically acclaimed drama about self-discovery and perseverance.</li>
            <li><em>Beyond the Horizon</em> (Director) - An adventurous sci-fi film exploring the unknown realms of space.</li>
            <li><em>City Lights</em> (Assistant) - A heartwarming romantic comedy set in the bustling streets of New York.</li>
          </ul>
        </Col>
      </Row>
      <Row className="mb-5">
        <Col>
          <h3>Skills</h3>
          <ul>
            <li>Project Management</li>
            <li>Script Development</li>
            <li>Team Coordination</li>
            <li>Creative Direction</li>
          </ul>
        </Col>
        <Col>
          <h3>Contact Information</h3>
          <p>
            Feel free to reach out to me at <a href={`mailto:${user.email}`}>{user.email}</a>. You can also find me on LinkedIn and GitHub.
          </p>
        </Col>
      </Row>
    </Container>
    
  );
};

export default withAuthenticationRequired(ProfileComponent, {
  onRedirecting: () => <Loading />,
});
