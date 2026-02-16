from rest_framework import serializers
from .models import Employee, Attendance


class EmployeeSerializer(serializers.ModelSerializer):

    def validate_employee_id(self, value):
        if Employee.objects.filter(employee_id=value).exists():
            raise serializers.ValidationError("Employee ID already exists.")
        return value

    class Meta:
        model = Employee
        fields = '__all__'


class AttendanceSerializer(serializers.ModelSerializer):
    employee_id = serializers.CharField(write_only=True)
    employee_name = serializers.CharField(
        source='employee.full_name',
        read_only=True
    )

    class Meta:
        model = Attendance
        fields = ['id', 'employee_id', 'employee_name', 'date', 'status']

    def validate_employee_id(self, value):
        if not Employee.objects.filter(employee_id=value).exists():
            raise serializers.ValidationError("Employee does not exist.")
        return value

    def validate(self, data):
        emp_id = data.get("employee_id")
        date = data.get("date")

        employee = Employee.objects.get(employee_id=emp_id)

        if Attendance.objects.filter(employee=employee, date=date).exists():
            raise serializers.ValidationError(
                "Attendance already marked for this date."
            )

        return data

    def create(self, validated_data):
        emp_id = validated_data.pop('employee_id')
        employee = Employee.objects.get(employee_id=emp_id)
        return Attendance.objects.create(employee=employee, **validated_data)
