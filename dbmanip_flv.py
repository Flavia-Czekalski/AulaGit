import sqlite3



def connect_db(db_name, logger):
    try:
        conn = sqlite3.connect(db_name + '.db')
        logger.info(f'Connetion stablished with DB: {db_name}.db')

        return conn


    except sqlite3.OperationalError:
        logger.error(f'Could not connect with {db_name}.db. Make sure the DB name is right')


def create_table(conn, logger):
    c = conn.cursor()

    try:
        c.execute('CREATE TABLE IF NOT EXISTS chipseq_Template(cell_type_category TEXT NOT NULL, '
                  'cell_type TEXT NOT NULL, cell_type_track_name TEXT NOT NULL, '
                  'cell_type_short TEXT NOT NULL, assay_category TEXT NOT NULL, assay TEXT NOT NULL, assay_track_name TEXT NOT NULL,'
                  'assay_short TEXT NOT NULL, donor TEXT NOT NULL, time_point TEXT NOT NULL, view TEXT NOT NULL,'
                  'track_name TEXT NOT NULL, track_type TEXT NOT NULL, track_density TEXT NOT NULL, provider_institution'
                  'TEXT NOT NULL, source_server TEXT NOT NULL, source_path_to_file TEXT NOT NULL, server TEXT NOT NULL,'
                  'path_to_file TEXT NOT NULL, new_file_name TEXT NOT NULL);')


        logger.info('Table project was created')

    except sqlite3.OperationalError:
        logger.error('Table project could not be created')


def insert_data(conn, list_of_data, logger):
    c = conn.cursor()

    try:
        with conn:
            for data in list_of_data:
                c.execute("INSERT INTO chipseq_Template VALUES(:cell_type_category,"
                          ":cell_type, :cell_type_track_name, :cell_type_short, :assay_category, :assay,"
                          ":assay_track_name, :assay_short, :donor, :time_point, :view, :track_name, :track_type,"
                          ":track_density, :provider_institution,"
                          ":source_server, :source_path_to_file, :server, :path_to_file, :new_file_name)", data)
            logger.info('Data was inserted on the DB')

    except sqlite3.OperationalError:
        logger.error('Data could not be inserted')


def update_assay(conn, assay, new_assay, logger):

    c = conn.cursor()

    try:
        with conn:
            c.execute("UPDATE chipseq_Template SET assay = :new_assay WHERE assay = :assay", {'assay': assay, 'new_assay': new_assay})
            logger.info(f'assay {assay} was updated for new_assay {new_assay}')

    except sqlite3.OperationalError:
        logger.error(f'COLD NOT UPDATE Assay:{assay} for new_assay: {new_assay}')

def update_donor(conn, donor, new_donor, logger):

    c = conn.cursor()

    try:
        with conn:
            c.execute("UPDATE chipseq_Template SET donor = :new_donor WHERE donor = :donor", {'donor': donor, 'new_donor': new_donor})
            logger.info(f'donor {donor} was updated for new_donor {new_donor}')

    except sqlite3.OperationalError:
        logger.error(f'COLD NOT UPDATE Donor:{donor} for donor: {new_donor}')


def select_cell_type(conn, logger):

    c = conn.cursor()

    try:
        with conn:
            c.execute("SELECT cell_type FROM Chipseq_Template")
            all_cell_type = c.fetchall()

            logger.info(f'Selected cell_type')
            return all_cell_type

    except sqlite3.OperationalError:
        logger.error(f'Could not Select cell_types. Check if the table exists.')



def select_all_track_name(conn, assay_track_name, logger):

    c = conn.cursor()

    try:
        with conn:
            c.execute("SELECT track_name FROM chipseq_Template WHERE assay_track_name = :assay_track_name", {"assay_track_name": assay_track_name})

            all_track_assay = c.fetchall()

            logger.info(f'Selected chipseq_Template with assay_track_name: {assay_track_name}')

            return all_track_assay

    except sqlite3.OperationalError:
        logger.error(f'Could not Select chipseq_Template assay. Check if the table exists.')


def select_all_cell_type_assay(conn, assay, logger):

    c = conn.cursor()

    try:
        with conn:
            c.execute("SELECT cell_type FROM chipseq_Template WHERE assay = :assay", {"assay": assay})

            all_cell_type_assay = c.fetchall()

            logger.info(f'Selected chipseq_Template with assay: {assay}')

            return all_cell_type_assay

    except sqlite3.OperationalError:
        logger.error(f'Could not Select chipseq_Template assay. Check if the table exists.')


def select_assay(conn, assay, logger):

    c = conn.cursor()

    try:
        with conn:
            c.execute("SELECT cell_type_track_name, track_name, track_type, track_density FROM chipseq_Template WHERE assay = :assay", {"assay": assay})

            all_assay = c.fetchall()

            logger.info(f'Selected chipseq_Template with assay: {assay}')

            return all_assay

    except sqlite3.OperationalError:
        logger.error(f'Could not Select chipseq_Template assay. Check if the table exists.')




def delete_track_name(conn, track_name, logger):
    c = conn.cursor()

    try:
        with conn:
            c.execute("DELETE FROM chipseq_Template WHERE  track_name = :track_name", {"track_name": track_name})

            logger.info(f'Rows where author is: "{track_name}",  were deleted')

    except sqlite3.OperationalError:
        logger.error(f'Could not delete {track_name}')