import argparse
import logging
import os
import sys
from db_util import dbmanip_flv as db
import util.loggerinitializer as utl

# Initialize log object
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
utl.initialize_logger(os.getcwd(), logger)


def main():
    parser = argparse.ArgumentParser(description="A Tool manipulate a sqlite DB")

    subparsers = parser.add_subparsers(title='actions',
                                       description='valid actions',
                                       help='Use sqlite-python.py {action} -h for help with each action',
                                       dest='command'
                                       )

    parser_index = subparsers.add_parser('createdb', help='Create database and tables')

    parser_index.add_argument("--db", dest='db', default=None, action="store", help="The DB name",
                        required=True)

    parser_insert = subparsers.add_parser('insert', help='Insert data on tables')

    parser_insert.add_argument("--file",  default=None, action="store", help="TSV file with the data to be inserted",
                        required=True)

    parser_insert.add_argument("--db", default=None, action="store", help="The DB name",
                        required=True)


    parser_update = subparsers.add_parser('update', help='Update a field in a db')

    parser_update.add_argument("--db", default=None, action="store", help="The DB name",
                        required=True)

    parser_update.add_argument("--assay", default=None, action="store", help="Name of assay",
                        required=False)

    parser_update.add_argument("--new_assay", default=None, action="store", help="Name of new_assay",
                        required=False)
    parser_update.add_argument("--donor", default=None, action="store", help="Name of donor",
                               required=False)

    parser_update.add_argument("--new_donor", default=None, action="store", help="Name of new_donor",
                               required=False)

    parser_select = subparsers.add_parser('select', help='Select  fields from the db')

    parser_select.add_argument("--db", default=None, action="store", help="The DB name",
                        required=True)

    parser_select.add_argument("--cell_type", action="store_true", help="Select all cell types",
                        required=False,default=False)

    parser_select.add_argument("-tn", action="store", help="Select all track name associated with a specific assay_track_name",
                        required=False,default=False)

    parser_select.add_argument("-ca", action="store", help="Select all cell_types associated with a assay",
                               required=False, default=False)

    parser_select.add_argument("-a", action="store", help="Select cell_type_track_name, track_name, track_type, track_density",
                        required=False, default=False)


    parser_delete = subparsers.add_parser('delete', help='delete rows from the db')

    parser_delete.add_argument("-d", default=False, action="store", help="Delete all records from a given track_name",
                        required=False)

    parser_delete.add_argument("--db", default=False, action="store", help="The DB name",
                        required=True)


    args = parser.parse_args()


    # sys.exit()
    conn = db.connect_db(args.db, logger)

    if args.command == "createdb":

        db.create_table(conn, logger)


    elif args.command == "insert":
        list_of_data = []

        with open(args.file, 'r') as f:
            for line in f:

                # reset dictionary
                line_dict = dict()

                # Skip empty lines
                if line.startswith(','):
                    continue


                # split line
                values = line.strip().split(',')

                # put each field in a dict
                line_dict['cell_type_category'] = values[0]
                line_dict['cell_type'] = values[1]
                line_dict['cell_type_track_name'] = values[2]
                line_dict['cell_type_short'] = values[3]
                line_dict['assay_category'] = values[4]
                line_dict['assay'] = values[5]
                line_dict['assay_track_name'] = values[6]
                line_dict['assay_short'] = values[7]
                line_dict['donor'] = values[8]
                line_dict['time_point'] = values[9]
                line_dict['view'] = values[10]
                line_dict['track_name'] = values[11]
                line_dict['track_type'] = values[12]
                line_dict['track_density'] = values[13]
                line_dict['provider_institution'] = values[14]
                line_dict['source_server'] = values[15]
                line_dict['source_path_to_file'] = values[16]
                line_dict['server'] = values[17]
                line_dict['path_to_file'] = values[18]
                line_dict['new_file_name'] = values[19]

                #append the dict to a list
                list_of_data.append(line_dict)

        db.insert_data(conn, list_of_data, logger)


    elif args.command == "update" and args.assay is not None:
        db.update_assay(conn, args.assay, args.new_assay, logger)

    elif args.command == "update" and args.donor is not None:
        db.update_donor(conn, args.donor, args.new_donor, logger)


    elif args.command == "select" and args.cell_type is not False:
        all_cell_type = db.select_cell_type(conn, logger)

        for cell_type in all_cell_type:
            print(cell_type)


    elif args.command == "select" and args.tn is not False:

        all_track_name = db.select_all_track_name(conn, args.tn, logger)


        print("\n| Track name")

        for i in all_track_name:
            print((i[0]))

    elif args.command == "select" and args.ca is not False:

        all_cell_type_assay = db.select_all_cell_type_assay(conn, args.ca, logger)


        print("\n| All_cell_type")

        for i in all_cell_type_assay:
            print(i[0])

    elif args.command == "select" and args.a is not False:

        all_assay = db.select_assay(conn, args.a, logger)


        print("\n| cell_type_track_name\t| track_name\t| track_type\t| track_density")

        for i in all_assay:
            print("|","\t| ".join(i))



    elif args.command == "delete":
        db.delete_track_name(conn, args.d, logger)


if __name__ == '__main__':
    main()




