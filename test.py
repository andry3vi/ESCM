
import escm_client as escm_c


def main():


        elog = escm_c.ESCM_client('ig-qad.igisol','Collinear')
        elog.new_message({'Author':'Germano','What':'testing'},'test')
        print(elog.queue[-1].answer)

        elog.send_last()

        print(elog.queue[-1].answer)

        elog.update_last('\nmah test 2')
        elog.send_last()

        print(elog.queue[-1].answer)
        elog.new_message({'Author':'Germano','What':'testing'},'test_new')
        elog.send_last()
        print(elog.queue[-1].answer)


if __name__ == '__main__':
    main()


