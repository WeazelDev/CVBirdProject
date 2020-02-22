from model.Marker import Markerfrom model.Frame import Framefrom scipy.optimize import least_squaresfrom scipy.linalg import normfrom scipy.spatial.transform import Rotationimport numpy as npclass CameraPosTracker():    '''        Manage the movements of the camera (position and rotation) along a video    '''        def __init__(self, frame0, init_pos = (0, 0, 0), init_rot = (0, 0, 0)):        """        Initialize the tracker        Parameters        ----------        init_pos : tuple of float, optional            Init position of the camera. The default is (0, 0, 0).        init_rot : tuple of float, optional            Initial rotation of the camera. The default is (0, 0, 0).        frame0 : Frame            Initial Frame information        Returns        -------        None.        """                self.cur_pos = init_pos        self.cur_rot = init_rot                self.pos_hist = [init_pos]        self.rot_hist = [init_rot]                self.ref_frame = frame0                    def computeMove(self, frame):        '''        Compute the camera move between self.ref_frame and frame        Parameters        ----------        frame : Frame            Frame induced by movement.        Returns        -------        new position and rotation        '''        markersPrev = self.ref_frame.getMarkersId()        markersNext = frame.getMarkersId()                commonMarkers = markersPrev.intersection(markersNext)                P1 = self.ref_frame.getMatrixPos(commonMarkers)        P2 = frame.getMatrixPos(commonMarkers)                #correct point with camera Rotation        P1_rot_mat = Rotation.from_rotvec(np.deg2rad(-self.ref_frame.camRot))        P2_rot_mat = Rotation.from_rotvec(np.deg2rad(-frame.camRot))                #print(P1.shape, P1_rot_mat.as_matrix().shape)                P1 = P1_rot_mat.as_matrix() @ P1.T        P2 = P1_rot_mat.as_matrix() @ P2.T                print('rot1', P1_rot_mat.as_euler('xyz', degrees=True))        print('rot2', P2_rot_mat.as_euler('xyz', degrees=True))                print(P1.shape)        print('p1', P1.T)        print('p2', P2.T)                new_pos = self.__solve_LS_camera_problem(P1.T, P2.T)                print('new pos', new_pos)            @staticmethod    def __least_square_camera_problem(X, P1, P2):        """        Formulate the problem we want to minimize :            SUM_OVER_N(NORM(X + P1 + P1)^2)            Parameters        ----------        X : array of float (size 3)            coordinate of the camera        P1 : matrix of size N x 3            Points location in frame 1        P2 : matrix of size N x 3            Points location in frame 2            Returns        -------        SUM_OVER_N(NORM(X + Quads_frame_1 + Quads_frame_2)^2)            """        #print(X + P2 - P1)        normed = norm(X + P2 - P1, axis = 1)        #print(normed)                return np.sum(normed)        def __solve_LS_camera_problem(self, P1, P2, X0=[0, 0, 0]):        """        Resolve the minimisation problem:            SUM_OVER_N(NORM(X + P1 + P1)^2)            Parameters        ----------        P1 : matrix of size N x 3            Points location in frame 1        P2 : matrix of size N x 3            Points location in frame 2        X0 : initial guess for X, optimally, previous positions            Returns        -------        X solution, None if no solution            """        res_lsq = least_squares(self.__least_square_camera_problem, X0, args=(P1, P2))                return res_lsq['x']            #%%def testCameraPosTracker():    frame = Frame(36)    frame.addMarkersAndRotFromJson()    tracker = CameraPosTracker(frame, init_pos = (-12488, -5843, 1038))    next_frame = Frame(37)    next_frame.addMarkersAndRotFromJson()    tracker.computeMove(next_frame)        frame = Frame(55)    frame.addMarkersAndRotFromJson()    tracker = CameraPosTracker(frame, init_pos = (-12488, -5843, 1038))    next_frame = Frame(56)    next_frame.addMarkersAndRotFromJson()    tracker.computeMove(next_frame)        