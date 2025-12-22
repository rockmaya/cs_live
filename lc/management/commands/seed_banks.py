from django.core.management.base import BaseCommand
from lc.models import Bank

BANKS = [
    {"name": "Eastern Bank PLC", "swift_code": "EBLDBDDH"},
    {"name": "ICD, IDB", "swift_code": ""},
    {"name": "Bank Asia PLC", "swift_code": "BALBBDDH"},
    {"name": "United Commercial Bank PLC", "swift_code": "UCBLBDDH"},
    {"name": "Al-Arafah Islami Bank PLC", "swift_code": "ALARBDDH"},
    {"name": "Standard Bank PLC", "swift_code": "SDBLBDDH"},
    {"name": "BRAC Bank PLC", "swift_code": "BRAKBDDH"},
    {"name": "Standard Chartered Bank", "swift_code": "SCBLBDDX"},
    {"name": "Pubali Bank PLC", "swift_code": "PUBABDDH"},
    {"name": "Uttara Bank PLC", "swift_code": "UTBLBDDH"},
    {"name": "Dhaka Bank PLC", "swift_code": "DHBLBDDH"},
    {"name": "Dutch-Bangla Bank PLC", "swift_code": "DBBLBDDH"},
    {"name": "Mercantile Bank PLC", "swift_code": "MBLBBDDH"},
    {"name": "Prime Bank PLC", "swift_code": "PRBLBDDH"},
    {"name": "Shahjalal Islami Bank PLC", "swift_code": "SJBLBDDH"},
    {"name": "Jamuna Bank PLC", "swift_code": "JAMUBDDH"},
    {"name": "Trust Bank PLC", "swift_code": "TTBLBDDH"},
    {"name": "Woori Bank Bangladesh", "swift_code": "HVBKBDDH"},
    {"name": "Southeast Bank PLC", "swift_code": "SEBDBDDH"},
    {"name": "NCC Bank PLC", "swift_code": "NCCLBDDH"},
    {"name": "One Bank PLC", "swift_code": "ONEBBDDH"},
    {"name": "IFIC Bank", "swift_code": "IFICBDDH"},
    {"name": "The City Bank PLC", "swift_code": "CIBLBDDH"},
    {"name": "Agrani Bank PLC", "swift_code": "AGBKBDDH"},
    {"name": "Janata Bank PLC", "swift_code": "JANBBDDH"},
    {"name": "Meghna Bank PLC", "swift_code": "MGBLBDDH"},
    {"name": "Community Bank Bangladesh PLC", "swift_code": "COYMBDDD"},
    {"name": "Midland Bank PLC", "swift_code": "MDBLBDDH"},
    {"name": "Mutual Trust Bank PLC", "swift_code": "MTBLBDDH"},
    {"name": "National Bank PLC", "swift_code": "NBLBBDDH"},
    {"name": "NRB Bank PLC", "swift_code": "NRBDBDDH"},
    {"name": "NRBC Bank PLC", "swift_code": "NRBBBDDH"},
    {"name": "Rupali Bank PLC", "swift_code": "RUPBBDDH"},
    {"name": "The Premier Bank PLC", "swift_code": "PRMRBDDH"},
    {"name": "Sonali Bank PLC", "swift_code": "BSONBDDH"},
    {"name": "Commercial Bank of Ceylon PLC", "swift_code": "CCEYBDDH"},
    {"name": "State Bank of India", "swift_code": "SBINBDDH"},
    {"name": "HSBC", "swift_code": "HSBCBDDH"},
]

class Command(BaseCommand):
    help = 'Seed bank list into the database'

    def handle(self, *args, **options):
        for bank_data in BANKS:
            bank, created = Bank.objects.update_or_create(
                name=bank_data['name'],
                defaults={'swift_code': bank_data['swift_code']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created bank: {bank.name}'))
            else:
                self.stdout.write(self.style.NOTICE(f'Updated bank: {bank.name}'))
